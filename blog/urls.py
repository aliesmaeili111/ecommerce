from django.urls import path
from blog.views import (home,article_detail,
                        CategoryList,AuthorList,
                        load_more_data_blog,load_more_data_comment,
                        ajax_save_comment,ajax_delete_comment,
                        add_new_like,load_article_likes)

app_name = 'blog'

urlpatterns = [
    path('home',home,name='home'),
    path('article/<slug>/',article_detail,name='detail'),
    path('category_blog/<slug>/',CategoryList.as_view(),name='category'),
    path('category_blog/<slug>/page/<int:page>/',CategoryList.as_view(),name='category'),
    path('author/<slug:username>/',AuthorList.as_view(),name='author'),
    path('author/<slug:username>/page/<int:page>/',AuthorList.as_view(),name='author'),

    path('load_more_data_blog',load_more_data_blog,name='load_more_data_blog'),
    
    path('load-comment',load_more_data_comment,name='load_more_data_comment'),

    path('ajax-save-comment/', ajax_save_comment,name="save-comment"),
    path('ajax-delete-comment/', ajax_delete_comment,name="delete-comment"),

    path('add_like/<slug>/', add_new_like,name="add_like"),
    path('likes-load/<slug>/', load_article_likes,name="likeLoad"),

]














