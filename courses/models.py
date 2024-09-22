from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.urls import reverse

from .fields import OrderField


# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("subject", args=[self.slug])


class Course(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="courses_created",
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        Subject, related_name="courses", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(
        default="images/default/default.jpg", upload_to="images/courses/%Y/%m/%d"
    )
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    course_description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="courses_joined", blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    has_completed = models.BooleanField(default=False)
    certification = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["title"]),
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})

    def courses_created_by_instructor(self):
        return self.owner.courses_created.count()

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return round(sum(rating.rating for rating in ratings) / ratings.count(), 1)
        return 0


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])

    def __str__(self):
        return f"{self.order}. {self.title}"

    class Meta:
        ordering = ["order"]


class Content(models.Model):
    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in": ("text", "video", "image", "file"),
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(blank=True, for_fields=["module"])

    class Meta:
        ordering = ["order"]


class ItemBase(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_related",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def render(self):
        return render_to_string(
            f"courses/content/{self._meta.model_name}.html", {"item": self}
        )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to="files")


class Image(ItemBase):
    file = models.FileField(upload_to="images")


class Video(ItemBase):
    url = models.URLField()


class Rating(models.Model):
    RATING_CHOICED = [
        (1, "1 - Poor"),
        (2, "2 - Fair"),
        (3, "3 - Good"),
        (4, "4 - Very Good"),
        (5, "5 - Excellent"),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="ratings")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICED)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("course", "user")
        verbose_name = "Ratitng"
        verbose_name_plural = "Ratings"

    def __str__(self):
        return f"{self.course.title} - {self.rating}"


class CourseProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="course_progress",
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course, related_name="progresses", on_delete=models.CASCADE
    )
    current_module = models.ForeignKey(
        Module,
        related_name="current_progress",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    completed_modules = models.ManyToManyField(
        Module, related_name="completed_progress", blank=True
    )
    completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} - {self.course}"

    def get_progress_percentage(self):
        total_modules = self.course.modules.count()
        if total_modules == 0:
            return 0
        completed_modules_count = self.completed_modules.count()
        return (completed_modules_count / total_modules) * 100


"""
def update_progress(student, course, module):
    progress, created = CourseProgress.objects.get_or_create(student=student, course=course)
    
    if module not in progress.completed_modules.all():
        progress.completed_modules.add(module)
    
    if progress.course.modules.count() == progress.completed_modules.count():
        progress.completed = True
    
    # Move to the next module (if exists)
    next_module = course.modules.filter(order__gt=module.order).first()
    progress.current_module = next_module if next_module else None
    progress.save()
"""
