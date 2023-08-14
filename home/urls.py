from django.urls import path
from home.views import (home,all_product,product_detail,
                        product_comment,
                        product_reply,comment_like,product_search
                        ,contact,load_more_data_comment,

                        add_new_like_product,load_product_likes,
                        delete_comment_product,
                        add_new_fav_product,load_product_fav
                        )


app_name = 'home'

urlpatterns = [
    path('',home,name='home'),
    path('products/',all_product,name='products'),
    path('detail/<slug>/<int:id>/',product_detail,name='detail'),
    path('detail/<slug>/<int:id>/page/<int:page>/',product_detail,name='detail'),
    path('category/<slug>/<int:id>/',all_product,name='category'),
    # path('like/<int:id>/',product_like,name='product_like'),
    # path('unlike/<int:id>/',product_unlike,name='product_unlike'),
    path('comment/<int:id>/',product_comment,name='product_comment'),
    path('reply/<int:id>/<int:comment_id>/',product_reply,name='product_reply'),
    path('like_comment/<int:id>/',comment_like,name='comment_like'),
    path('search/',product_search,name='product_search'),
    # path('favourite/<slug>/<int:id>/',favourite_product,name='favourite'),
    path('contact/',contact,name='contact'),
    path('load_more_data_comment',load_more_data_comment,name='load_more_data_comment'),
    
    
    path('add_like_product/<slug>/<int:id>/',add_new_like_product,name='add_new_like_product'),
    path('load_product_likes/<slug>/<int:id>/',load_product_likes,name='load_product_likes'),

    path('delete-comment-product/',delete_comment_product,name='ajax_delete_comment_product'),


    path('add-fav-product/<slug>/<int:id>/',add_new_fav_product,name='add_new_fav_product'),
    path('load-fav-product/<slug>/<int:id>/',load_product_fav,name='load_product_fav'),


]
