from django import template
from ..models import Cart

register = template.Library()


@register.inclusion_tag('partials/cart_select.html',takes_context=True)
def cart(context):
    request = context['request']
    cart = Cart.objects.filter(user_id=request.user.id)
    total = 0
    for p in cart :
        if p.product.status != 'None':
            total += p.variant.total_price * p.quantity
        else:
            total += p.product.total_price * p.quantity
    context = {
        'cart':cart,
        'total':total,
        'request':request,
    }
    return context
