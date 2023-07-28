from django import template
from ..models import Category

register = template.Library()

@register.inclusion_tag('partials/category_side.html')
def category_side():
    return  {
        'category': Category.objects.filter(status=True),
    }

    