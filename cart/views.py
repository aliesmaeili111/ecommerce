from django.shortcuts import render,get_object_or_404,redirect
from home.models import Product,Variants
from cart.models import Cart,CartForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from order.models import OrderForm

# Cart detail views
@login_required(login_url='accounts:login')
def cart_detail(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    user = request.user
    form = OrderForm()
    total = 0
    for p in cart :
        if p.product.status != 'None':
            total += p.variant.total_price * p.quantity
        else:
            total += p.product.total_price * p.quantity
    context = {
        'cart':cart,
        'total':total,
        'form':form,
        'user':user
    }
    return render(request,'cart/cart.html',context)

# Add Cart detail views
@login_required(login_url='accounts:login')
def add_cart(request,id):
    url = request.META.get("HTTP_REFERER")
    product = Product.objects.get(id=id)
    if product.status != 'None':
        var_id = request.POST.get('select')
        data = Cart.objects.filter(user_id=request.user.id,variant_id=var_id)
        if data:
            check = 'yes'
        else:
            check ='no'
    else:
        data = Cart.objects.filter(user_id=request.user.id,product_id=id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    
    if request.method == "POST":
        form = CartForm(request.POST)
        var_id = request.POST.get('select')
        if form.is_valid():
            info = form.cleaned_data['quantity']
            if check == 'yes':
                if product.status != 'None':
                    shop = Cart.objects.get(user_id=request.user.id,product_id=id,variant_id=var_id)
                    messages.success(request,'Add to cart','success')
                else:
                    shop = Cart.objects.get(user_id=request.user.id,product_id=id)
                    messages.success(request,'Add to cart','success')
             
                shop.quantity += info
                shop.save()
            else:
                Cart.objects.create(user_id=request.user.id,
                                    product_id=id,
                                    variant_id=var_id,
                                    quantity=info)
                messages.success(request,'Add to cart','success')
        return redirect(url)


@login_required(login_url='accounts:login')
def remove_cart(request,id):
    url = request.META.get("HTTP_REFERER")
    Cart.objects.filter(id=id).delete()
    return redirect(url)
    