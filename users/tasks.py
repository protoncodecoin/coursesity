import logging
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from celery import shared_task
from .tokens import generate_token

# logger = logging.getLogger(__name__)


@shared_task(bind=True)
def send_welcome_email(self, user_id):
    try:
        unverified_user = get_user_model().objects.get(id=user_id)
        # logger.info(f"Unverified user is {unverified_user}")

        subject = "Welcome to Coursesity"
        message = f"Hello {unverified_user.first_name}!\n\nThank you for choosing Coursesity. There are exciting opportunities awaiting you!"
        from_email = settings.EMAIL_HOST_USER

        sent_email = send_mail(
            subject,
            message,
            from_email,
            [unverified_user.email],
            fail_silently=True,
        )
        return sent_email
    except Exception as e:
        # print(str(e))  # should be logged not printed
        raise self.retry(exc=e, countdown=5)


@shared_task(bind=True)
def send_activation_email(self, user_id, domain):
    try:
        unverified_user = get_user_model().objects.get(id=user_id)

        from_email = settings.EMAIL_HOST_USER
        to_list = [unverified_user.email]

        email_subject = "Confirm Your Email Address"
        messages2 = render_to_string(
            "registration/confirmation.html",
            {
                "name": unverified_user.first_name,
                "domain": domain,
                "uid": urlsafe_base64_encode(force_bytes(unverified_user.pk)),
                "token": generate_token.make_token(unverified_user),
            },
        )

        mail_sent = send_mail(
            email_subject, messages2, from_email, to_list, fail_silently=False
        )
        # logger.info(f"Activation email sent: {mail_sent}")
        return mail_sent
    except Exception as e:
        # logger.error(f"Couldn't send the mail: {e}")
        # print(str(e))
        raise self.retry(exc=e, countdown=True)
