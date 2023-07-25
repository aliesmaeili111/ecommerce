from django.urls import path
from home.views import (home,all_product,product_detail,
                        product_like,product_unlike,product_comment,
                        product_reply,comment_like,product_search,
                        favourite_product,contact)


app_name = 'home'

urlpatterns = [
    path('',home,name='home'),
    path('products/',all_product,name='products'),
    path('detail/<slug>/<int:id>/',product_detail,name='detail'),
    path('category/<slug>/<int:id>/',all_product,name='category'),
    path('like/<int:id>/',product_like,name='product_like'),
    path('unlike/<int:id>/',product_unlike,name='product_unlike'),
    path('comment/<int:id>/',product_comment,name='product_comment'),
    path('reply/<int:id>/<int:comment_id>/',product_reply,name='product_reply'),
    path('like_comment/<int:id>/',comment_like,name='comment_like'),
    path('search/',product_search,name='product_search'),
    path('favourite/<slug>/<int:id>/',favourite_product,name='favourite'),
    path('contact/',contact,name='contact'),

]
