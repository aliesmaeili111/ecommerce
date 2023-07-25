from django.db import models
from home.models import Product,Variants
from django.contrib.auth.models import User
from django.forms import ModelForm


class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='انتخاب محصول')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='انتخاب کاربر')
    variant = models.ForeignKey(Variants,on_delete=models.CASCADE,blank=True,null=True,verbose_name='انتخاب گونه محصول')
    quantity = models.PositiveIntegerField(verbose_name='تعداد')


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'کارت'
        verbose_name_plural = 'کارت ها'

class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']
        
        

class Compare(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='انتخاب کاربر',blank=True, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='انتخاب محصول')
    session_key = models.CharField(max_length=300,blank=True, null=True,verbose_name='کلید مقایسه')


    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'مقایسه'
        verbose_name_plural = 'مقایسه محصولات'
        

class CompareForm(ModelForm):
    class Meta:
        model = Compare
        fields = ['product']
        