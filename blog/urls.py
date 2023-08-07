from django.urls import path
from blog.views import (ArticleList,article_detail,
                        CategoryList,AuthorList,load_more_data_blog)

app_name = 'blog'

urlpatterns = [
    path('',ArticleList.as_view(),name='home'),
    path('page/<int:page>/',ArticleList.as_view(),name='home'),
    path('article/<slug>/',article_detail,name='detail'),
    path('category_blog/<slug>/',CategoryList.as_view(),name='category'),
    path('category_blog/<slug>/page/<int:page>/',CategoryList.as_view(),name='category'),
    path('author/<slug:username>/',AuthorList.as_view(),name='author'),
    path('author/<slug:username>/page/<int:page>/',AuthorList.as_view(),name='author'),
]
