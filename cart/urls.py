from django.urls import path
from cart.views import (cart_detail,add_cart,remove_cart,
                        add_single,remove_single,
                        compare,show,remove_compare,
                        # cart_add
                        )


app_name = 'cart'

urlpatterns = [
    path('',cart_detail,name='cart_detail'),
    # path('add/',cart_add,name='add'),
    path('add/<int:id>/',add_cart,name='add_cart'),
    path('remove/<int:id>/',remove_cart,name='remove_cart'),
    path('add_single/<int:id>/',add_single,name='add_single'),
    path('remove_single/<int:id>/',remove_single,name='remove_single'),
    path('compare/<int:id>/',compare,name='compare'),
    path('show/',show,name='show'),
    path('remove_compare/<int:id>/',remove_compare,name='remove_compare'),
]
