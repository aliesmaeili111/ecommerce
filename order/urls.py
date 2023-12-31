from django.urls import path
from order.views import (order_detail,
                        order_create,coupon_order,
                        order_information,
                        # send_request,verify
                        )
app_name = 'order'

urlpatterns = [
    path('<int:order_id>/',order_detail,name='order_detail'),
    path('create/',order_create,name='order_create'),
    path('coupon/<int:order_id>/',coupon_order,name='coupon'),
    path('order/information/',order_information,name='order_information'),

    # path('request/<int:order_id>/<int:price>/',send_request,name='request'),
    # path('verify/',verify,name='verify'),
]
