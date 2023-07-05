from django.db import models
from django.contrib.auth.models import User
from home.models import Variants,Product
from django.forms import ModelForm


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField()
    f_name = models.CharField(max_length=300)
    l_name = models.CharField(max_length=300)
    address = models.CharField(max_length=400)
    
    def __str__(self):
        return self.user.username
    
    def get_price(self):
        total = sum(i.price() for i in self.order_item.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total
    
    
class Coupon(models.Model):
    code = models.CharField(unique=True,max_length=20)
    active = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    discount = models.PositiveIntegerField()


class ItemOrder(models.Model):
    order = models.ForeignKey(Order,related_name='order_item',on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants,on_delete=models.CASCADE,blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
   
    
    def __str__(self):
        return self.user.username
    
    def size(self):
        return self.variant.size_variant.name
    
    def color(self):
        return self.variant.color_variant.name
    
    def price(self):
        if self.product.status != None:
            return self.variant.total_price * self.quantity
        else:
            return self.product.total_price * self.quantity
        
        
class OrderForm(ModelForm):
    class Meta :
        model = Order
        fields = ['email','f_name','l_name','address']
        