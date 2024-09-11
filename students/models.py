from django.db import models
from django.conf import settings

from courses.models import Course

# Create your models here.


class WishList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="wishlist", on_delete=models.CASCADE
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.get_full_name()} added {self.course.title} to wishlist"
