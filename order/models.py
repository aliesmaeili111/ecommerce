from django.db import models
from django.contrib.auth.models import User
from home.models import Variants,Product
from django.forms import ModelForm
from django_jalali.db import models as jmodels
from extensions.utils import jalali_conveter


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='کاربر')
    create = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False,verbose_name='پرداخت شده')
    code = models.CharField(max_length=300,verbose_name='کد سفارش',blank=True)
    discount = models.PositiveIntegerField(blank=True, null=True,verbose_name='درصد تخفیف')
    email = models.EmailField(verbose_name='ایمیل')
    f_name = models.CharField(max_length=300,verbose_name='نام')
    l_name = models.CharField(max_length=300,verbose_name='نام خانوادگی')
    address = models.CharField(max_length=400,verbose_name='آدرس')
    
    def __str__(self):
        return self.user.username
    
    def get_price(self):
        total = sum(i.price() for i in self.order_item.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total
    get_price.short_description = 'قیمت'
    
    def jpublish(self):
        return jalali_conveter(self.create)
    jpublish.short_description = "زمان سفارش"

    
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
    
    
class Coupon(models.Model):
    code = models.CharField(unique=True,max_length=20,verbose_name='کد تخفیف')
    active = models.BooleanField(default=False,verbose_name='فعال')
    start = jmodels.jDateTimeField(verbose_name='شروع کد تخفیف')
    end = jmodels.jDateTimeField(verbose_name='پایان کد تخفیف')
    discount = models.PositiveIntegerField(verbose_name='درصد تخفیف')
    
    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'کدتخفیف'
        verbose_name_plural = 'کد تخفیف ها'

class ItemOrder(models.Model):
    order = models.ForeignKey(Order,related_name='order_item',on_delete=models.CASCADE,verbose_name='سفارش')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='محصول')
    variant = models.ForeignKey(Variants,on_delete=models.CASCADE,blank=True, null=True,verbose_name='گونه')
    quantity = models.PositiveIntegerField(default=0,verbose_name='تعداد')
   
    
    def __str__(self):
        return self.user.username
    
    def size(self):
        return self.variant.size_variant.name
    
    def color(self):
        return self.variant.color_variant.name
    
    def price(self):
        if self.product.status != 'None':
            return self.variant.total_price * self.quantity
        else:
            return self.product.total_price * self.quantity
        
    class Meta:
        verbose_name = 'مورد سفارش'
        verbose_name_plural = 'مورد سفارشات'
        
        
class OrderForm(ModelForm):
    class Meta :
        model = Order
        fields = ['email','f_name','l_name','address']
        