from datetime import timedelta
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import Count, Sum
from django.core.validators import MinValueValidator
from django.utils import timezone

from courses.models import Course

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
        upload_to="users/%Y/%m/%d", blank=True, default="users/default.jpeg"
    )
    slug = models.SlugField(blank=True, null=True)
    linkedIn = models.URLField(blank=True, null=True)
    x = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

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

    def num_of_courses(self):
        return self.courses_created.count()

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "":
            self.slug = slugify(self.get_full_name())
        super(CustomUser, self).save(args, kwargs)


class Profile(models.Model):

    # class Interest(models.TextChoices):
    #     ANY = "any", "Any"
    #     SCIENCE = "science", "science"
    #     MATH = "mathematics", "Mathematics"
    #     CYBERSECURITY = "cybersecurity", "Cybersecurity"
    #     PROGRAMMING = "programming", "Programming"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    field_of_study = models.IntegerField(default=1)
    # interest = models.CharField(max_length=100, choices=Interest, default=Interest.ANY)

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
    institution = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name}"


class Meeting(models.Model):
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="host", on_delete=models.CASCADE
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    meeting_name = models.CharField(max_length=100, blank=True)
    meeting_token = models.UUIDField(help_text="meeting token")
    date_created = models.DateTimeField(auto_now_add=True)
    sch_date = models.DateField(blank=True, null=True)
    sch_time = models.TimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    only_enrolled_students = models.BooleanField(
        default=True, help_text="allow only enrolled students in the meeting"
    )
    expires = models.DateTimeField(default=timezone.now() + timedelta(days=3))
    about_message = models.TextField(blank=True)

    def __str__(self):
        return f"meeting hosted by {self.host.get_full_name}"
