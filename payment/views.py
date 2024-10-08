from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from courses.models import Course
from orders.models import Order

from .models import Payment, UserWallet


# Create the stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


# def payment_process(request):
#     order_id = request.session.get("order_id")
#     order = get_object_or_404(Order, id=order_id)

#     if request.method == "POST":
#         success_url = request.build_absolute_uri(
#             reverse(
#                 "payment:completed",
#             )
#         )

#         cancel_url = request.build_absolute_uri(
#             reverse("payment:canceled"),
#         )
#         # Stripe checkout session data
#         session_data = {
#             "mode": "payment",
#             "client_reference_id": order.id,
#             "success_url": success_url,
#             "cancel_url": cancel_url,
#             "line_items": [],
#         }

#         # add order items to the stripe checkout session
#         for item in order.items.all():
#             session_data["line_items"].append(
#                 {
#                     "price_data": {
#                         "unit_amount": int(item.price * Decimal("100")),
#                         "currency": "usd",
#                         "product_data": {
#                             "name": item.course.title,
#                         },
#                     },
#                     "quantity": item.quantity,
#                 }
#             )

#         # create stripe checkout session
#         session = stripe.checkout.Session.create(**session_data)
#         # redirect to stripe payment form
#         return redirect(session.url, code=303)
#     return render(request, "payment/process.html", locals())


def payment_completed(request):
    courses = request.session.get("added_courses")
    # get the id of the courses and and the current user
    # add current user to courses they paid for
    curr_user = request.user
    for i in courses:
        course_obj = Course.objects.filter(id=i).first()
        course_obj.students.add(curr_user)
        course_obj.save()

    # clear courses from session
    del request.session["added_courses"]
    return render(request, "payment/completed.html")


def payment_canceled(request):
    # clear courses from session
    del request.session["added_courses"]
    return render(request, "payment/canceled.html")


def initiate_payment(request):
    if request.method == "POST":
        amount = request.POST["amount"]
        email = request.user.email

        pk = settings.PAYSTACK_PUBLIC_KEY
        payment = Payment.objects.create(amount=amount, email=email, user=request.user)
        payment.save()

        context = {
            "payment": payment,
            "field_values": request.POST,
            "paystack_pub_key": pk,
            "amount_value": payment.amount_value(),
        }
        return render(request, "", context)
    return render(request, "payment.html")


def verify_payment(request, ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()

    if verified:
        user_wallet = UserWallet.objects.get(user=request.user)
        user_wallet.balance += payment.amount
        user_wallet.save()
        print(request.user.get_full_name(), " paid for the course")
        return render(request, "success.html")
    return render(request, "failed.html")
