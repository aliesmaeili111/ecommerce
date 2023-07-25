from django import template
from ..models import Category,Product,Variants

register = template.Library()

# filter for pagination urlencode
@register.simple_tag()
def filter_url(number,name,urlencode=None):
    url = '?{}={}'.format(name,number)
    if urlencode:
        sp_query = url.split('&')
        sp_filter = filter(lambda x:x.split('=')[0] != name,sp_query)
        join_query = '&'.join(sp_filter)
        url = '{}&{}'.format(url,join_query)
    return url

# show category in all pages 
@register.inclusion_tag('partials/category_navbar.html')
def category_navbar():
    return {
        'category':Category.objects.filter(sub_cat=False),
    }
    
# show all products in home page
@register.inclusion_tag('partials/all_prodcuts.html',takes_context=True)
def all_prodcuts(context):
    request = context['request']
    return {
        'products': Product.objects.all().order_by('-create')[:6],
        'sell': Product.objects.all().order_by('-sell')[:6],
        'request':request,
    }
    
    
@register.inclusion_tag('partials/tags.html')
def tags():
    return {
        'category':Category.objects.filter(sub_cat=False),
    }
