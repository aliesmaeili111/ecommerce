from django.shortcuts import render,get_object_or_404,redirect
from home.models import Product,Variants
from django.contrib import messages
# compare for product with session
# from cart.compare import NewCompare
from cart.cart import NewCart
from cart.forms import CartAddForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse


# Cart detail views
# @login_required(login_url='accounts:login')
def cart_detail(request):
    total = 0
    cart = NewCart(request)
    for c in cart:
        total += int(c['variant'].total_price * c['quantity'] )

    return render(request,'cart/newcart.html',{"cart":cart,"total":total})


@require_POST
def cart_add(request):
    variant_id = request.POST.get('select')
    variant = get_object_or_404(Variants,id=variant_id)
    cart = NewCart(request)
    form = CartAddForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(variant=variant,quantity=data['quantity'])
    
    return redirect('cart:cart_detail')
    



def cart_remove(request,id):
    variant = get_object_or_404(Variants,id=id)
    cart = NewCart(request)
    cart.remove(variant=variant)
    return redirect('cart:cart_detail')
    

def new_add_single(request):
    variant_id = request.GET.get('variant_id')
    variant = get_object_or_404(Variants,id=variant_id)
    cart = NewCart(request)
    cart.add(variant=variant,quantity=1)
    cart.save()
    data = {'suucess':'ok'}
    return JsonResponse(data)


def cart_show(request):
    total , price , quantity , discount = 0, 0 , 0 ,0
    cart = NewCart(request)
    for c in cart:
        total += int(c['variant'].total_price * c['quantity'] )
        price += int(c['variant'].unit_price * c['quantity'] )
        quantity += c['quantity'] 
        discount = price - total
    response = {"total":total,"price":price,"quantity":quantity,"discount":discount}
    return JsonResponse(response)


# Add Cart detail views
# @login_required(login_url='accounts:login')
# def add_cart(request,id):
#     url = request.META.get("HTTP_REFERER")
#     product = Product.objects.get(id=id)
#     if product.status != 'None':
#         var_id = request.POST.get('select')
#         data = Cart.objects.filter(user_id=request.user.id,variant_id=var_id)
#         if data:
#             check = 'yes'
#         else:
#             check ='no'
#     else:
#         data = Cart.objects.filter(user_id=request.user.id,product_id=id)
#         if data:
#             check = 'yes'
#         else:
#             check = 'no'
    
#     if request.method == "POST":
#         form = CartForm(request.POST)
#         var_id = request.POST.get('select')
#         if form.is_valid():
#             info = form.cleaned_data['quantity']
#             if check == 'yes':
#                 if product.status != 'None':
#                     shop = Cart.objects.get(user_id=request.user.id,product_id=id,variant_id=var_id)
#                     messages.success(request,'Add to cart','success')
#                 else:
#                     shop = Cart.objects.get(user_id=request.user.id,product_id=id)
#                     messages.success(request,'Add to cart','success')
             
#                 shop.quantity += info
#                 shop.save()
#             else:
#                 Cart.objects.create(user_id=request.user.id,
#                                     product_id=id,
#                                     variant_id=var_id,
#                                     quantity=info)
#                 messages.success(request,'Add to cart','success')
#         return redirect(url)


# @login_required(login_url='accounts:login')
# def remove_cart(request,id):
#     url = request.META.get("HTTP_REFERER")
#     Cart.objects.filter(id=id).delete()
#     return redirect(url)
    
    
# def add_single(request,id):
#     url = request.META.get("HTTP_REFERER")
#     cart = Cart.objects.get(id=id)
#     if cart.product.status == 'None':
#         product = Product.objects.get(id=cart.product.id)
#         if product.amount > cart.quantity:
#             cart.quantity += 1
#             messages.success(request,'Add one other product','success')
#         else:
#             messages.error(request,'You cant Add one other product','danger')
#     else:
#         variant = Variants.objects.get(id=cart.variant.id)
#         if variant.amount > cart.quantity:
#             cart.quantity += 1
#             messages.success(request,'Add one other product','success')
#         else:
#             messages.error(request,'You cant Add one other product','danger')
#     cart.save()
#     # data = {'suucess':'ok'}
#     # return JsonResponse(data)
#     return redirect(url)



#  def remove_single(request,id):
#     url = request.META.get("HTTP_REFERER")  
#     cart = Cart.objects.get(id=id)
#     if cart.quantity < 2 :
#         cart.delete()
#     else:
#         cart.quantity -= 1
#         cart.save()
#     return redirect(url)



# def compare(request,id):
#     url = request.META.get("HTTP_REFERER")  
#     if request.user.is_authenticated:
#         item = get_object_or_404(Product,id=id)
#         qs = Compare.objects.filter(user_id=request.user.id,product_id=id)
#         if qs.exists():
#             messages.success(request,'Add to compare','success')
#         else:
#             Compare.objects.create(user_id=request.user.id,
#                                    product_id=item.id,
#                                    session_key=None
#                                    )
#     else:
#         item = get_object_or_404(Product,id=id)
#         qs = Compare.objects.filter(user_id=None,product_id=id,session_key=request.session.session_key)
#         if qs.exists():
#             messages.success(request,'Add to compare','success')
#         else:
#             if not request.session.session_key:
#                 request.session.create()
#             Compare.objects.create(user_id=None,
#                                    product_id=item.id,
#                                    session_key=request.session.session_key
#                                    )
#     return redirect(url)
    
    
# def show(request):
#     if request.user.is_authenticated:
#         data = Compare.objects.filter(user_id=request.user.id)
#         return render(request,'cart/show.html',{'data':data,})
#     else:
#         data = Compare.objects.filter(session_key__exact=request.session.session_key,user_id=None)
#         return render(request,'cart/show.html',{'data':data,})
    
    
# @login_required(login_url='accounts:login')
# def remove_compare(request,id):
#     url = request.META.get("HTTP_REFERER")
#     compare = get_object_or_404(Compare,id=id)
#     compare.delete()
#     messages.error(request,'You compare remove','danger')
#     return redirect(url)

     

# Run Comapare page with session

# def add_new_compare(request,slug,product_id):
#     product = get_object_or_404(Product,slug=slug,id=product_id)
#     data = NewCompare(request)
#     data.add(product=product)
#     messages.success(request,'add producr for compare','success')
#     return redirect('home:home')

# def remove_new_compare(request,slug,product_id):
#     product = get_object_or_404(Product,slug=slug,id=product_id)
#     data = NewCompare(request)
#     data.remove(product=product)
#     messages.success(request,'remove producr for compare','success')
#     return redirect('cart:new_compare')

# def new_compare(request):
#     data = NewCompare(request)
#     return render(request,'cart/compare.html',{'data':data})


