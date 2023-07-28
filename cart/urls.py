from django.urls import path
from cart.views import (cart_detail,
                        # add_cart,remove_cart,
                        # add_single,remove_single,
                        # compare,show,
                        # remove_compare,
                        cart_add,cart_remove,new_add_single,cart_show,
                        # new_compare,add_new_compare,remove_new_compare
                        )


app_name = 'cart'

urlpatterns = [
    # session for cart
    path('',cart_detail,name='cart_detail'),
    path('newadd/',cart_add,name='newadd'),
    path('newremove/<int:id>/',cart_remove,name='newremove'),
    path('new_add_single/',new_add_single,name='new_add_single'),
    path('cart_show/',cart_show,name='cart_show'),


    # path('add/<int:id>/',add_cart,name='add_cart'),
    # path('remove/<int:id>/',remove_cart,name='remove_cart'),
    
    # path('add_single/<int:id>/',add_single,name='add_single'),
    # path('remove_single/<int:id>/',remove_single,name='remove_single'),

    # path('compare/<int:id>/',compare,name='compare'),
    # path('show/',show,name='show'),
    # path('remove_compare/<int:id>/',remove_compare,name='remove_compare'),

    # session for compare    

    # path('newcompare/',new_compare,name='new_compare'),
    # path('add/<slug>/<int:product_id>/',add_new_compare,name='add_new_compare'),
    # path('remove/<slug>/<int:product_id>/',remove_new_compare,name='remove_new_compare')
]

