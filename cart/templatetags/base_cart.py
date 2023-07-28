from django import template
from cart.cart import NewCart
from django.http import JsonResponse


register = template.Library()
    

@register.inclusion_tag('partials/cart_select.html',takes_context=True)
def cart(context):
    request = context['request']
    total = 0
    cart = NewCart(request)
    for c in cart:
        total += int(c['variant'].total_price * c['quantity'] )
    context = {
        'cart':cart,
        'total':total,
        'request':request,
    }
    return context
