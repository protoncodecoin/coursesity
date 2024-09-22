from django import template
from django.contrib.auth import get_user_model
from students.models import WishList

register = template.Library()


@register.filter
def add_to_wishlist(obj, id):
    User = get_user_model()
    try:
        user_obj = User.objects.get(email=obj)
    except (WishList.DoesNotExist, User.DoesNotExist):
        return None
    if WishList.objects.filter(user=user_obj, id=id).exists():
        return True
    return False
