from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import Count, Sum
from django.core.validators import MinValueValidator

from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_disabled = models.BooleanField(
        default=False, help_text="Check to disable user account"
    )
    is_instructor = models.BooleanField(
        default=False, help_text="Checked creates an instructor account"
    )
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d", blank=True, default="users/default.jpg"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_total_number_of_enrolled_student(self):
        if self.is_instructor:
            qs = self.courses_created.annotate(num_of_students=Count("students"))
            return qs.aggregate(total=Sum("num_of_students"))["total"]
        else:
            return None


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    photo = models.ImageField(upload_to="users/%Y/%m/%d", blank=True)

    def __str__(self):
        return f"Profile of {self.user.email}"


class InstructorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="instructor_profile",
    )
    biography = models.TextField()
    years_of_experience = models.IntegerField(
        validators=[MinValueValidator(1)], default=1
    )

    def __str__(self):
        return f"{self.user.get_full_name}"
