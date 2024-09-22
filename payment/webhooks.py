import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from courses.models import Course
from courses.recommender import Recommender

from .tasks import payment_complete


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event.type == "checkout.session.completed":
        session = event.data.object

        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=400)

            # mark order as paid
            order.paid = True

            # store stripe id
            order.stripe_id = session.payment_intent
            order.save()

            # save courses bought for product reccomendataions
            courses_ids = order.items.values_list("course_id")
            courses = Course.objects.filter(id__in=courses_ids)
            r = Recommender()
            r.courses_bought(courses)

            # launch asynchronous task
            payment_complete.delay(order.id)

    return HttpResponse(status=200)
