from django.urls import path

from . import views
from . import webhooks

app_name = "payment"

urlpatterns = [
    # path("process/", views.payment_process, name="process"),
    path("completed/", views.payment_completed, name="completed"),
    path("canceled/", views.payment_canceled, name="canceled"),
    path("webhook/", webhooks.stripe_webhook, name="stripe-webhook"),
    # paystack
    path("initiate-payment/", views.initiate_payment, name="initiate_payment"),
    path("verify-payment/<str:ref>/", views.verify_payment, name="verify_payment"),
]
