from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from colorfield.fields import ColorField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.db.models import Avg


# Category model
class Category(models.Model):
    sub_category = models.ForeignKey('self',related_name='sub',on_delete=models.CASCADE,blank=True, null=True)
    sub_cat = models.BooleanField(default=False)
    name = models.CharField(max_length=150,blank=True, null=True)
    slug = models.SlugField(unique=True,allow_unicode=True,blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    update = models.DateTimeField(auto_now=True,blank=True, null=True)
    image = models.ImageField(upload_to='category',blank=True, null=True)
    
    def __str__(self):
        return self.name
  
    def get_absolute_url(self):
        return reverse('home:category',args=[self.slug,self.id])
  
  
# Product model   
class Product(models.Model):
    
    VARIANT = (
        ('None','none'),
        ('Size','size'),
        ('Color','color'),
    )
    
    category = models.ManyToManyField(Category,blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,allow_unicode=True,blank=True, null=True)
    image = models.ImageField(upload_to='product')
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    information = RichTextUploadingField(blank=True, null=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    available = models.BooleanField(default=True)
    status = models.CharField(blank=True, null=True,max_length=200,choices=VARIANT)
    like = models.ManyToManyField(User,blank=True,related_name='product_like')
    total_like = models.PositiveIntegerField(default=0)
    
    unlike = models.ManyToManyField(User,blank=True,related_name='product_unlike')
    total_unlike = models.PositiveIntegerField(default=0)
    
    
    
    def __str__(self):
        return self.name
    
    def average(self):
        data = Comment.objects.filter(is_reply=False,product=self).aggregate(avg=Avg('rate'))
        star = 0 
        if data['avg'] is not None:
            star = round(data['avg'],1)
        return star
            
            
    
    
    def get_absolute_url(self):
        return reverse('home:detail',args=[self.slug,self.id])
    
    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price
    
    def total_like(self):
        return self.like.count()
    
    def total_unlike(self):
        return self.unlike.count()
    
    
    
# Size model
class Size(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
  
# Color model  
class Color(models.Model):
    color = ColorField(default='#fff')
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name
    
# Variants model
class Variants(models.Model):
    name = models.CharField(max_length=100)
    product_variant = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='pr')
    size_variant = models.ForeignKey(Size,on_delete=models.CASCADE,null=True,blank=True)
    color_variant = models.ForeignKey(Color,on_delete=models.CASCADE,null=True,blank=True)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True,blank=True)
    total_price = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name

    
    @property
    def total_price(self):
        if not self.discount :
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price   
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    comment = RichTextUploadingField()
    rate = models.PositiveIntegerField(default=1)
    create = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self',related_name='comment_reply',on_delete=models.CASCADE,blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    comment_like = models.ManyToManyField(User,related_name='com_like',blank=True)
    total_comment_like = models.PositiveIntegerField(default=0)
    
    
    def total_comment_like(self):
        return self.comment_like.count()
    
    
    def __str__(self):
        return self.product.name


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment','rate']
        
class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
      
      
class Images(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True)
    image = models.ImageField(upload_to='images/',blank=True)
    
    def __str__(self):
        return self.product.name
    
    
