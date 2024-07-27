from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem, Order

from django.contrib.auth import get_user_model


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

            # get details from database and create order and orderitem
            new_order_item = Order.objects.create(
                first_name=user.first_name, last_name=user.last_name, email=user.email
            )
            for item in cart:
                OrderItem.objects.create(
                    order=new_order_item, course=item["course"], price=item["price"]
                )
            # clear the cart
            cart.clear()
            return render(
                request, "orders/order/created.html", {"order": new_order_item}
            )

        request.session["next"] = request.path
        return redirect("student_registration")

    return render(request, "orders/order/create.html", {"cart": cart})
