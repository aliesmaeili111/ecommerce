from django.shortcuts import get_object_or_404
from blog.models import Article,Category
from django.views.generic import ListView,DetailView
from django.contrib.auth.models import User

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


class AuthorList(ListView):
    paginate_by = 1
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User,username=username)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context

