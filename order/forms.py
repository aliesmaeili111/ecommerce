from django import forms
from order.models import Coupon

class CouponForm(forms.Form):
    code = forms.CharField(max_length=20)
    