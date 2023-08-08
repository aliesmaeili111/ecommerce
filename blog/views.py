from django.shortcuts import get_object_or_404,render
from blog.models import Article,Category
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import JsonResponse


def home(request):
    article_list = Article.objects.published().order_by('-id')[:2]
    total_article = Article.objects.count()

    context = {
        'object_list':article_list,
        'total_article':total_article,
    }
    return render(request,'blog/article_list.html',context)

def load_more_data_blog(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    article = Article.objects.all().order_by('-id')[offset:offset+limit]
    t = render_to_string('blog/ajax/list.html',{'data':article})
    return JsonResponse({'data':t})


def article_detail(request,slug):
    article = get_object_or_404(Article.objects.published(),slug=slug)
    similar = article.tag.similar_objects()[:3]
    context = {
        'article':article,
        'similar':similar,
        "tag": article.tag.all(),
    }
    return render(request,'blog/article_detail.html',context)

# class ArticleDetail(DetailView):
#     def get_object(self):
#         slug = self.kwargs.get('slug')
#         return get_object_or_404(Article.objects.published(),slug=slug)
        
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

