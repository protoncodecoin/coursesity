from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from courses.models import Course
from .cart import Cart


# Create your views here.
@require_POST
def cart_add(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    # The course is automatically added to the cart if a post request is sent
    # add the course to the cart
    cart.add(course=course)

    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    cart.remove(course)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})
