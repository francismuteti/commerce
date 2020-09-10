from django.contrib import admin

# Register your models here.
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code','valid_from','valid_to','discount','active']