import django_filters
from home.models import Product,Brand,Color,Size
from django import forms


class ProductFilter(django_filters.FilterSet):
    choices_1 = {
        ('گران ترین',' گران ترین'),
        ('ارزان ترین','ارزان ترین'),
    }
    
    choices_2 = {
        ('قدیمی ترین','قدیمی ترین'),
        ('جدید ترین','جدید ترین'),
    }
    
    choices_3 = {
        ('dis','کم تخفیف'),
        ('پر تخفیف','پر تخفیف'),
    }
    
    choices_4 = {
        ('s','کم فروش'),
        ('پر فروش ترین','پر فروش ترین'),
    }
    
    choices_5 = {
        ('f','کم محبوب'),
        ('محبوب ترین','محبوب ترین'),
    }
    
    choices_6 = {
        ('v','کم بازدید ترین'),
        ('پر بازدید ترین','پر بازدید ترین'),
    }
    
    price_1 = django_filters.NumberFilter(field_name='unit_price',lookup_expr='gte')
    price_2 = django_filters.NumberFilter(field_name='unit_price',lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(),widget=forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(),widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(),widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices=choices_1 ,method='price_filter')
    create = django_filters.ChoiceFilter(choices=choices_2 ,method='create_filter')
    discount = django_filters.ChoiceFilter(choices=choices_3 ,method='discount_filter')
    sell = django_filters.ChoiceFilter(choices=choices_4 ,method='sell_filter')
    favourite = django_filters.ChoiceFilter(choices=choices_5 ,method='favourite_filter')
    view = django_filters.ChoiceFilter(choices=choices_6 ,method='views_filter')
    
    
    def price_filter(self,queryset,nama,value):
        data = 'unit_price' if value == 'ارزان ترین' else '-unit_price'
        return queryset.order_by(data)
    
    def create_filter(self,queryset,nama,value):
        data = 'create' if value == 'قدیمی ترین' else '-create'
        return queryset.order_by(data)
    
    def discount_filter(self,queryset,nama,value):
        data = 'discount' if value == 'dis' else '-discount'
        return queryset.order_by(data)
    
    def sell_filter(self,queryset,nama,value):
        data = 'sell' if value == 's' else '-sell'
        return queryset.order_by(data)
    
    def favourite_filter(self,queryset,nama,value):
        data = 'total_favourite' if value == 'f' else '-total_favourite'
        return queryset.order_by(data)
    
    
    def views_filter(self,queryset,nama,value):
        data = 'num_view' if value == 'v' else '-num_view'
        return queryset.order_by(data)
    