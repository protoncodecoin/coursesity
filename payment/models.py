from django.utils import timezone
from django.db import models
from django.conf import settings
import secrets
from decimal import Decimal

from .paystack import Paystack


# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    reference_code = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

    def amount_value(self):
        return Decimal(self.amount) * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result["amount"] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False

    def __str__(self):
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref

        super().save(*args, **kwargs)
