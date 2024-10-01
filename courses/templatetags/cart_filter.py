from django import template
from django.conf import settings

from cart import cart


register = template.Library()


@register.filter
def check_object_in_cart(request, obj):
    cart_obj = cart.Cart(request)
    ids = [item["course"].id for item in cart_obj]

    return True if obj in ids else False
