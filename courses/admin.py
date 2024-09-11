from django.contrib import admin

# Register your models here.
from .models import Subject, Course, Module, Rating


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "subject", "created", "updated", "price"]
    list_filter = ["created", "subject"]
    list_editable = ["price"]
    search_fields = ["title", "overview"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = [
        "course",
        "user",
        "rating",
    ]

    list_filter = [
        "rating",
        "user",
    ]
