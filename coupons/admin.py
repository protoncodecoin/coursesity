from django.contrib import admin

from coupons.models import Coupon


# Register your models here.
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "valid_from",
        "discount",
        "active",
    ]
    list_filter = ["active", "valid_from", "valid_to"]
    search_fields = ["code"]
