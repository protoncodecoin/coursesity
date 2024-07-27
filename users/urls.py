from django.urls import path

from . import views


urlpatterns = [
    path(
        "register/",
        views.UserRegisterView.as_view(),
        name="user_registration",
    ),
    path("login/", views.UserLoginView.as_view(), name="login"),
    #activate account
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate"),
]
