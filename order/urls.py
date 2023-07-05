from django.urls import path
from order.views import order_detail,order_create,coupon_order

app_name = 'order'

urlpatterns = [
    path('<int:order_id>/',order_detail,name='order_detail'),
    path('create/',order_create,name='order_create'),
    path('coupon/<int:order_id>/',coupon_order,name='coupon'),
]
