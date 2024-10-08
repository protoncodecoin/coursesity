from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.http import HttpResponse

import stripe
import requests

from cart.cart import Cart
from payment.models import Payment


from .forms import OrderCreateForm
from .models import OrderItem, Order
from .tasks import course_order_created

# Create the stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/orders/order/detail.html", {"order": order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/order/pdf.html", {"order": order})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order_{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(finders.find("css/pdf.css"))]
    )
    return response


# Create your views here.
# @login_required(login_url="student_registration")
def order_create(request):
    cart = Cart(request)
    # check if the user is logged in
    # copy and save session to be used later
    # if not redirect the user to login
    # save session back in the browser

    if request.method == "POST":
        if request.user.is_authenticated:
            user = get_object_or_404(get_user_model(), pk=request.user.id)
            payment_option = request.POST.get("payment_option", "paystack")
            print(payment_option)

            # get details from database and create order and orderitem
            new_order_item = Order.objects.create(
                first_name=user.first_name, last_name=user.last_name, email=user.email
            )
            if cart.coupon:
                new_order_item.coupon = cart.coupon
                new_order_item.discountt = cart.coupon.discount

                new_order_item.save()

            course_ids = list()
            for item in cart:
                OrderItem.objects.create(
                    order=new_order_item, course=item["course"], price=item["price"]
                )
                course_ids.append(item["course"].id)
                # request.session["added_courses"] = course_ids
                # clear the cart
                # cart.clear()

                # launch asychronous task
                # course_order_created.delay(new_order_item.id)

                # set the order in the session
                # request.session["order_id"] = new_order_item.id
                # return redirect("payment:process")

                # get the order id
                # build success url
            if payment_option == "stripe":

                success_url = request.build_absolute_uri(
                    reverse(
                        "payment:completed",
                    )
                )

                cancel_url = request.build_absolute_uri(
                    reverse("payment:canceled"),
                )
                # Stripe checkout session data
                session_data = {
                    "mode": "payment",
                    "client_reference_id": new_order_item.id,
                    "success_url": success_url,
                    "cancel_url": cancel_url,
                    "line_items": [],
                }

                # add order items to the stripe checkout session
                for item in new_order_item.items.all():
                    session_data["line_items"].append(
                        {
                            "price_data": {
                                "unit_amount": int(item.price * Decimal("100")),
                                "currency": "usd",
                                "product_data": {
                                    "name": item.course.title,
                                },
                            },
                            "quantity": item.quantity,
                        }
                    )

                # stripe coupon
                if new_order_item.coupon:
                    stripe_coupon = stripe.Coupon.create(
                        name=new_order_item.coupon.code,
                        percent_off=new_order_item.discountt,
                        duration="once",
                    )
                    session_data["discounts"] = [{"coupon": stripe_coupon.id}]

                # create stripe checkout session
                session = stripe.checkout.Session.create(**session_data)
                # redirect to stripe payment form
                return redirect(session.url, code=303)

            if payment_option == "paystack":
                print("going for paystack=======================")
                secret_key: str = settings.PAYSTACK_SECRET_KEY
                headers: dict = {
                    "authorization": f"Bearer {secret_key}",
                    "content-type": "application/json",
                }

                # total_amount: int = new_order_item.get_total_cost() * 1_0000

                URL: str = "https://api.paystack.co/transaction/initialize"

                body: dict = {
                    "amount": 100_000,
                    "currency": "GHS",
                    "email": user.email,
                }

                # send a request to the paystack api to initiate a transaction
                response = requests.post(URL, headers=headers, json=body)
                print(response.json(), "this is the response --------------")
                response = response.json()
                status = response["status"]
                if status == True:
                    print("initialization was succesfful =======================")
                    # save access_code in the model
                    # send access code to the frontend to continue transaction
                    Payment.objects.create(
                        user=user,
                        amount=10000,
                        ref=response["data"]["reference"],
                        access_code=response["data"]["access_code"],
                        authorization_url=response["data"]["authorization_url"],
                    )
                else:
                    return redirect("orders:order_create")
                # return to the paystack payment page
                return render(
                    request,
                    "orders/paystack/paystack.html",
                    {"access_code": response["data"]["access_code"]},
                )

        request.session["next"] = request.path
        return redirect("user_registration")

    return render(
        request,
        "orders/order/create.html",
        {
            "cart": cart,
        },
    )


def paystack_payment(request):
    # initialize transaction
    secret_key = settings.PAYSTACK_SECRET_KEY
    headers = {
        "authorization": f"Bearer {secret_key}",
        "content-type": "application/json",
    }

    body = {"amount": "", "currency": "GHS", "email": "useremail"}
