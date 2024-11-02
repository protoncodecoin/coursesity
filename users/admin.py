from django.contrib import admin


from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, InstructorProfile, Meeting, Profile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_instructor",
        "is_disabled",
        "photo",
        "linkedIn",
        "x",
        "website",
        "slug",
    )
    list_filter = ("email", "is_staff", "is_active", "is_instructor", "is_disabled")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_instructor",
                    "is_disabled",
                    "photo",
                    "first_name",
                    "last_name",
                    "slug",
                    "linkedIn",
                    "x",
                    "website",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_disabled",
                    "photo",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        # "interest",
        "field_of_study",
    ]


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "years_of_experience",
        "institution",
        "biography",
    ]


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = [
        "host",
        "course",
        "only_enrolled_students",
        "meeting_token",
        "date_created",
        "updated",
        "expires",
        "about_message",
    ]
