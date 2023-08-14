from django.shortcuts import get_object_or_404,render
from blog.models import Article,Category,Comment
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from time import sleep


def home(request):
    article_list = Article.objects.published().order_by('-id')[:9]
    article = Article.objects.published().order_by('-id').count()
    total_article = Article.objects.count()
    comment_count = Comment.objects.filter(active=True,article=article).count()

    context = {
        'object_list':article_list,
        'total_article':total_article,
        'comment_count':comment_count,
    }
    return render(request,'blog/article_list.html',context)

# load more article
def load_more_data_blog(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    article = Article.objects.published().order_by('-id')[offset:offset+limit]
    sleep(2)
    t = render_to_string('blog/ajax/list.html',{'data':article})
    return JsonResponse({'data':t})


# load more comment
def load_more_data_comment(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    slug =str (request.GET['slug'])
    article = get_object_or_404(Article.objects.published(),slug=slug)
    comment = Comment.objects.filter(active=True,article=article).order_by('-id')[offset:offset+limit]
    sleep(2)
    t = render_to_string('blog/ajax/list_article_comment.html',{'data':comment})
    return JsonResponse({'data':t})


# load save comment
def ajax_save_comment(request):
    if request.method == "POST":
        pk = request.POST.get('id')
        
        comment = request.POST.get('comment')
        article = Article.objects.get(id=pk)
        user = request.user
        
        new_comment = Comment.objects.create(comment=comment,user=user,article=article,active=True)
        new_comment.save()
        response = 'Comment Posted'
        return HttpResponse(response)


# load delete comment
@csrf_exempt
def ajax_delete_comment(request):
    if request.method == "POST":
        id = request.POST.get('cid')
        comment = Comment.objects.get(id=id)
        comment.delete()
        
        return JsonResponse({"status":1})
    
    else:
        return JsonResponse({"status":2})

# add new like for comment
def add_new_like(request,slug):

    article = get_object_or_404(Article.objects.published(),slug=slug)
    user = request.user

    if user in article.likes.all():
        article.likes.remove(user)
        like_response = "<i class='fa fa-thumbs-up'></i>"
        return JsonResponse(like_response,safe=False,status=200)
    else:
        article.likes.add(user)
        like_response = "<i class='text-success fa fa-thumbs-up'></i>"
        return JsonResponse(like_response,safe=False,status=200)


# load like for article
def load_article_likes(request,slug):
    article = get_object_or_404(Article.objects.published(),slug=slug)
    likes_list = list(article.likes.values())
    return JsonResponse(likes_list,safe=False,status=200)


def article_detail(request,slug):
    article = get_object_or_404(Article.objects.published(),slug=slug)
    similar = article.tag.similar_objects()[:3]
    comment = Comment.objects.filter(active=True,article=article).order_by('-date')[:10]
    comment_count = Comment.objects.filter(active=True,article=article).count()
    total_comment = Comment.objects.filter(active=True).count()
    
    context = {
        'article':article,
        'similar':similar,
        "tag": article.tag.all(),
        "comment":comment,
        "comment_count":comment_count,
        "total_comment":total_comment,
    }

    return render(request,'blog/article_detail.html',context)        
class CategoryList(ListView):
    paginate_by = 12
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
    paginate_by = 12
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
