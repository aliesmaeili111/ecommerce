from django.shortcuts import render,get_object_or_404,redirect
from home.models import (Category,Product,Variants,
                        Comment,CommentForm,ReplyForm,
                        Images,Chart,Views,Gallery,Brand)
from django.contrib import messages
from home.forms import SearchForm
from django.db.models import Q,Max,Min
from cart.models import CartForm
from cart.forms import CartAddForm
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from home.filters import ProductFilter
from urllib.parse import urlencode
from django.http import JsonResponse
from blog.models import Article
from django.template.loader import render_to_string
from time import sleep


def home(request):
    category = Category.objects.filter(sub_cat=False)
    gallery = Gallery.objects.all()
    brand = Brand.objects.all()
    articles = Article.objects.filter(status='p').order_by('-publish')[:4]
    context = {
        'category':category,
        'gallery':gallery,
        'brand':brand,
        'articles':articles,
    }
    return render(request,'home/home.html',context)
    
    
def all_product(request,slug=None,id=None):

    products = Product.objects.all().order_by('-id')
    Filter = ProductFilter(request.GET,queryset=products)
    products = Filter.qs

    min_ = Product.objects.aggregate(unit_price=Min('unit_price'))
    min_price = int(min_['unit_price'])
    max_ = Product.objects.aggregate(unit_price=Max('unit_price'))
    max_price = int(max_['unit_price'])
    
    paginator = Paginator(products,2)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    
    form = SearchForm()
    category = Category.objects.filter(sub_cat=False)
    

    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data['search']
            page_obj = products.filter(Q(name__icontains=data))
            paginator = Paginator(page_obj,1)
            page_num = request.GET.get('page')
            data = request.GET.copy()
            if 'page' in data :
                del data['page']
            page_obj = paginator.get_page(page_num)
            
            
    if slug and id :
        data = get_object_or_404(Category,slug=slug,id=id)
        products = Product.objects.filter(category=data).order_by('-id')
        Filter = ProductFilter(request.GET, queryset=products)
        products = Filter.qs
        paginator = Paginator(products, 2)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

    context = {
        'products':page_obj,
        'category':category,
        'form':form,
        'page_num':page_num,
        'filter':Filter,
        'min_price':min_price,
        'max_price':max_price,
    }

    return render(request,'home/products.html',context)
    



def product_detail(request,slug,id,page=1):
    product = get_object_or_404(Product,slug=slug,id=id)
    form = CartAddForm()
    ip = request.META.get('REMOTE_ADDR')
    view = Views.objects.filter(product_id=product.id,ip=ip)
    if not view.exists():
        Views.objects.create(product_id=product.id,ip=ip)
        product.num_view += 1
        product.save()
        
    if request.user.is_authenticated:
        product.view.add(request.user)
    update = Chart.objects.filter(product_id=id)
    change = Chart.objects.all()
    images = Images.objects.filter(product_id=id)
    similar = product.tags.similar_objects()[:5]
    comment_form = CommentForm()
    reply_form = ReplyForm()
    cart_form = CartForm()
    data_comment = Comment.objects.filter(product_id=id,is_reply=False)
    paginator_comment = Paginator(data_comment,3)
    comment = paginator_comment.get_page(page)

    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True
    
    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        is_unlike = True
    
    # is_favourite = False
    # if product.favourite.filter(id=request.user.id).exists():
    #     is_favourite = True    
    
    context = {
            'product':product,
            'similar':similar,
            'is_like':is_like,
            'is_unlike':is_unlike,
            'data_comment':data_comment,
            'comment_form':comment_form,
            'comment':comment,
            'reply_form':reply_form,
            'images':images,
            'cart_form':cart_form,
            # 'is_favourite':is_favourite,
            'change':change,
            'form':form,
            'update':update,
        }
    

    if request.method == "POST":
        variant = Variants.objects.filter(product_variant_id=id)
        var_id = request.POST.get('select')
        variants = Variants.objects.get(id=var_id)
        colors = Variants.objects.filter(product_variant_id=id,size_variant_id=variants.size_variant_id)
        size = Variants.objects.filter(product_variant_id=id).distinct('size_variant_id')
    else:
        variant = Variants.objects.filter(product_variant_id=id)
        variants = Variants.objects.get(id=variant[0].id)
        colors = Variants.objects.filter(product_variant_id=id,size_variant_id=variants.color_variant_id)
        size = Variants.objects.filter(product_variant_id=id).distinct('size_variant_id')
        
    context.update({'variant':variant,'variants':variants,'colors':colors,'size':size})
    return render(request,'home/product_detail.html',context)



# like product
def product_like(request,id):
    url = request.META.get("HTTP_REFERER")
    product = get_object_or_404(Product,id=id)
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
        is_like = False
        messages.error(request,'remove ','danger')
    else:
        product.like.add(request.user)
        is_like = True
        messages.success(request,'add ','success')
    
    return redirect(url)

# Dislike product
def product_unlike(request,id):
    
    url = request.META.get("HTTP_REFERER")
    product = get_object_or_404(Product,id=id)
    product.unlike.add(request.user)
    messages.error(request,'you cant change dislike to like','danger')
    
    return redirect(url)


def product_comment(request,id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(comment=data['comment'],
                                   rate=data['rate'],
                                   user_id=request.user.id,
                                   product_id=id)
            messages.success(request,'نظر شما با موفقیت ثبت شد','success')
            return redirect(url)

        

def product_reply(request,id,comment_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Comment.objects.create(comment=data['comment'],
                                   user_id=request.user.id,
                                   product_id=id,
                                   reply_id=comment_id,
                                   is_reply=True,
                                   )
            
            messages.success(request,'ممنونیم از پاسخ شما','success')
            return redirect(url)
        
        
def comment_like(request,id):
    url = request.META.get("HTTP_REFERER")
    comment = get_object_or_404(Comment,id=id)
    if comment.comment_like.filter(id=request.user.id).exists():
        comment.comment_like.add(request.user)
        messages.error(request,'like comment give','danger')
        return redirect(url)
    else:
        comment.comment_like.add(request.user) 
        messages.success(request,'thanks for like Comment','success')
        return redirect(url)  
    
    
def product_search(request):
    products = Product.objects.all()
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['search']
            if data.isdigit():
                products = products.filter(Q(discount__exact=data)|Q(unit_price__exact=data))
            else:
                products = products.filter(Q(name__icontains=data))
            context = {
                'form':form,
                'products':products,
            }
            return render(request,'home/products.html',context)
        
        
def favourite_product(request,slug,id):
    # url = request.META.get("HTTP_REFERER")
    product = get_object_or_404(Product,slug=slug,id=id)
    # is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
        product.total_favourite -= 1
        # is_favourite = False
        messages.error(request,'you wishlist remove','danger')
    else:
        product.favourite.add(request.user)
        product.total_favourite += 1
        # is_favourite = True
        messages.success(request,'you wishlist added','success')
    product.save()
    data = {'success':'OK'}
    return JsonResponse(data)


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        subject = request.POST['subject']
        email = request.POST['email']
        msg = request.POST['message']
        body = name + '\n' + subject + '\n' + email + '\n' + msg
        form = EmailMessage(
            'Contact Form',
            body,
            'test',
            ('aliesmaeili11@gmailcom',),
        )
        form.send(fail_silently=False)

    return render(request,'home/contact.html')
