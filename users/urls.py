from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user_registration"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    # reset password
    path(
        "password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # change password
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "profile/<int:user_id>/<slug:user_slug>/",
        views.showProfile,
        name="show_profile",
    ),
    # activate account
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate"),
]
