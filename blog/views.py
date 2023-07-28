from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from blog.models import Article,Category
from django.core.paginator import Paginator
from django.views.generic import ListView,DetailView


class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 1
    

class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(),slug=slug)


class CategoryList(ListView):
    paginate_by = 1
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(),slug=slug)
        return category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_blog'] = category
        return context

