from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon,CouponForm

# Create your views here.
def CouponApply(request):
    now = timezone.now()
    coupon = CouponForm(request.POST)
    if request.method =='POST':
        code = Coupon.code
        code ==request.POST['code']
       
        try:
            coupon = Coupon.objects.get(code__iexact=code,valid_from__lte=now,valid_to__gte=now,active=True)
            
        except Coupon.DoesNotExist:
           coupon=None
    return redirect('duka:cart')    