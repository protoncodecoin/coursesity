from io import BytesIO
import weasyprint
from celery import shared_task
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from orders.models import Order
from django.conf import settings


@shared_task(bind=True)
def payment_complete(self, order_id):
    """
    Task to send an e-mail notification when an order is successfully paid
    """
    try:
        order = Order.objects.get(id=order_id)
        # create an invoice e-mail
        subject = f"Coursity - Invoice no. {order.id}"
        message = "Please, find attached the invoice for your recent purchase."
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.email])

        # generate PDF
        html = render_to_string("orders/order/pdf.html", {"order": order})
        out = BytesIO()

        # Get the CSS path correctly
        css_path = finders.find("css/pdf.css")
        if isinstance(css_path, list):
            css_path = css_path[0]  # Use the first path if multiple

        stylesheets = [weasyprint.CSS(css_path)]
        weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

        # attach PDF file
        email.attach(f"order_{order.id}.pdf", out.getvalue(), "application/pdf")

        # send e-mail
        email.send()
    except Exception as e:
        raise self.retry(exc=e, countdown=5)
