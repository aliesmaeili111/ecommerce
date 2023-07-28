from django.shortcuts import render,redirect,get_object_or_404
from order.models import OrderForm,Order,ItemOrder,Coupon
from cart.models import Cart
from django.contrib.auth.decorators import login_required
from order.forms import CouponForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from suds import Client
from django.http import HttpResponse
from home.models import Variants
import jdatetime
from django.utils.crypto import get_random_string
from kavenegar import *
from cart.cart import NewCart
from cart.views import cart_remove

def order_information(request):
    form = OrderForm() 
    return render(request,'order/order.html',{'form':form})


def order_detail(request,order_id):
    order = Order.objects.get(id=order_id)
    form = CouponForm()
    context = {
        'order':order,
        'form':form,
    }
    return render(request,'order/orders.html',context)


@login_required(login_url='acounts:login')
def order_create(request):
    if request.method == 'POST' :
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            code = get_random_string(length=8)
            order = Order.objects.create(user_id=request.user.id,email=data['email'],
            f_name=data['f_name'],
            l_name=data['l_name'],
            address=data['address'],
            code = code)
            
            cart = NewCart(request)
            for c in cart:
                ItemOrder.objects.create(order_id=order.id,user_id=request.user.id,
                                        variant=c['variant'],
                                        price=c['price'],
                                        quantity = c['quantity'])
        messages.success(request,'Your Order Successfuly.Thanks','success')
        return redirect('order:order_detail',order.id)


@require_POST
def coupon_order(request,order_id):
    form = CouponForm(request.POST)
    time = jdatetime.datetime.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,start__lte=time,end__gte=time,active=True)
        except Coupon.DoesNotExist:
            messages.error(request,'This code wrong','danger')
            return redirect('order:order_detail',order_id) 
        
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
        messages.success(request,'This code ok','success')
    return redirect('order:order_detail',order_id) 



# MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# mobile = '09371595811'  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://127.0.0.1:8000/order/verify/'
 

# def send_request(request,price,order_id):
#     global amount , o_id
#     amount = price
#     o_id = order_id
#     result = client.service.PaymentRequest(MERCHANT,amount,description,request.user.email,mobile,CallbackURL)
#     if result.Status == 100:
#         return redirect('https://www.zarinpal.com/pg/StartPay/') + str(result.Authority)
#     else:
#         return HttpResponse('Error code :' + str(result.Status))


# def verify(request):
#     if request.GET.get('Status') == 'Ok':
#         result = client.service.PaymentVerification(MERCHANT,request.GET['Authority'],amount)
#         if result.Status == 100:

#             # start in remover one as session cart
#             cart = Cart(request)
#             for c in cart :
#                 variants = Variants.objects.filter(id=c['varinat'].id)
#                 for data in variants :
#                     data.amount -= c['quantity']
#                     data.save()
#             messages.success(request,'Paid success','success')
#             return redirect('home:home')
#             # end in remover one as session cart
            
#         elif result.Status == 101:
#             return HttpResponse('transaction submitted :' + str(result.Status))
#         else:
#             return HttpResponse('transaction failed' + str(result.Status))
#     else:
#         return HttpResponse('transaction failed or canceled by user ')
