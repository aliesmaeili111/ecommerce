from django.urls import path
from blog.views import ArticleList,ArticleDetail,CategoryList

app_name = 'blog'

urlpatterns = [
    path('',ArticleList.as_view(),name='home'),
    path('page/<int:page>/',ArticleList.as_view(),name='home'),
    path('article/<slug>/',ArticleDetail.as_view(),name='detail'),
    path('category_blog/<slug>/',CategoryList.as_view(),name='category'),
    path('category_blog/<slug>/page/<int:page>/',CategoryList.as_view(),name='category'),
]
