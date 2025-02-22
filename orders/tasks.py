from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order


@shared_task(bind=True)
def course_order_created(self, order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    try:
        order = Order.objects.get(id=order_id)
        subject = f"Order nr. {order.id}"
        message = f"Dear {order.first_name},\n\nYou Keep pushing for success.\n\nYour order ID is {order.id}"
        mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
        return mail_sent
    except Exception as e:
        raise self.retry(exc=e, countdown=5)
