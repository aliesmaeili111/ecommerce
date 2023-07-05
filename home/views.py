from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from home.models import Category,Product,Variants,Comment,CommentForm,ReplyForm,Images
from django.contrib import messages
from home.forms import SearchForm
from django.db.models import Q
from cart.models import CartForm

def home(request):
    category = Category.objects.filter(sub_cat=False)
    context = {
        'category':category,
    }
    return render(request,'home/home.html',context)
    
    
def all_product(request,slug=None,id=None):
    products = Product.objects.all()
    form = SearchForm()
    category = Category.objects.filter(sub_cat=False)
    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data['search']
            products = products.filter(Q(name__icontains=data))
            
    if slug and id :
        data = get_object_or_404(Category,slug=slug,id=id)
        products = products.filter(category=data)
    
    context = {
        'products':products,
        'category':category,
        'form':form,
    }
    return render(request,'home/products.html',context)


def product_detail(request,slug,id):
    product = get_object_or_404(Product,slug=slug,id=id)
    images = Images.objects.filter(product_id=id)
    similar = product.tags.similar_objects()[:5]
    comment_form = CommentForm()
    reply_form = ReplyForm()
    cart_form = CartForm()
    comment = Comment.objects.filter(product_id=id,is_reply=False)
    
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True
    
    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        is_unlike = True
        
    if product.status != 'None':
        if request.method == "POST":
            variant = Variants.objects.filter(product_variant_id=id)
            var_id = request.POST.get('select')
            variants = Variants.objects.get(id=var_id)
        else:
            variant = Variants.objects.filter(product_variant_id=id)
            variants = Variants.objects.get(id=variant[0].id)
        context = {
            'product':product,
            'variant':variant,
            'variants':variants,
            'similar':similar,
            'is_like':is_like,
            'is_unlike':is_unlike,
            'comment_form':comment_form,
            'comment':comment,
            'reply_form':reply_form,
            'images':images,
            'cart_form':cart_form,
        }  
        return render(request,'home/product_detail.html',context)
    else:
    
        context = {
            'product':product,
            'similar':similar,
            'is_like':is_like,
            'is_unlike':is_unlike,
            'comment_form':comment_form,
            'comment':comment,
            'reply_form':reply_form,
            'images':images,
            'cart_form':cart_form,
        }
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
            messages.success(request,'add comment','success')
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
            
            messages.success(request,'thanks for reply Comment','success')
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
        