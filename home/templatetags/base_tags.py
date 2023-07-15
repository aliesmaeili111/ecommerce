from django import template
from ..models import Category,Product,Variants

register = template.Library()

@register.inclusion_tag('partials/category_navbar.html')
def category_navbar():
    return {
        'category':Category.objects.filter(sub_cat=False),
    }
    
    
@register.inclusion_tag('partials/all_prodcuts.html',takes_context=True)
def all_prodcuts(context):
    request = context['request']
    return {
        'products': Product.objects.all().order_by('-create')[:6],
        'request':request,
    }
