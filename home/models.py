from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from colorfield.fields import ColorField
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm
from taggit.managers import TaggableManager
from django.db.models import Avg
from extensions.utils import jalali_conveter
from django_jalali.db import models as jmodels
from django.db.models.signals import post_save 
from django.utils import timezone
from django.utils.safestring import mark_safe


# Manager for active category
class CategoryManager(models.Manager):
    def active(self):
        return self.filter(sub_cat=False)
    
    def sub_true(self):
        return self.filter(sub_cat=True)
    

# Category model
class Category(models.Model):
    sub_category = models.ForeignKey('self',related_name='sub',on_delete=models.CASCADE,blank=True, null=True,verbose_name='زیر دسته بندی')
    sub_cat = models.BooleanField(default=False,verbose_name='آیا زیر دسته بندی است ؟')
    name = models.CharField(max_length=150,blank=True, null=True,verbose_name='نام دسته بندی')
    slug = models.SlugField(unique=True,allow_unicode=True,blank=True, null=True,verbose_name='آدرس دسته بندی')
    create = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    update = jmodels.jDateTimeField(auto_now=True,blank=True, null=True)
    image = models.ImageField(upload_to='category',blank=True, null=True,verbose_name='تصویر دسته بندی')

    
    def __str__(self):
        return self.name
  
    def get_absolute_url(self):
        return reverse('home:category',args=[self.slug,self.id])
    
    def jpublish_create(self):
        return jalali_conveter(self.create)
    jpublish_create.short_description = "زمان انتشار دسته بندی "
        
    # Rename model
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها ' 
        
    objects = CategoryManager()
  
# Product model   
class Product(models.Model):
    
    VARIANT = (
        ('None','none'),
        ('Size','size'),
        ('Color','color'),
        ('Both','Both'),
    )
    
    category = models.ManyToManyField(Category,blank=True,verbose_name='دسته بندی')
    name = models.CharField(max_length=200,verbose_name='نام محصول')
    slug = models.SlugField(unique=True,allow_unicode=True,blank=True, null=True,verbose_name='آدرس محصول')
    image = models.ImageField(upload_to='product',verbose_name='تصویر محصول')
    amount = models.PositiveIntegerField(verbose_name='تعداد محصول')
    unit_price = models.PositiveIntegerField(verbose_name='قیمت محصول')
    change = models.BooleanField(default=True,verbose_name='عوض کردن')
    information = RichTextUploadingField(blank=True, null=True,verbose_name='جزئیات محصول')
    discount = models.PositiveIntegerField(blank=True, null=True,verbose_name='درصد تخفیف محصول')
    total_price = models.PositiveIntegerField(verbose_name='قیمت کل',blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)
    update = jmodels.jDateTimeField(auto_now=True)
    tags = TaggableManager(blank=True,verbose_name='تگ')
    available = models.BooleanField(default=True,verbose_name='فعال')
    status = models.CharField(blank=True, null=True,max_length=200,choices=VARIANT,verbose_name='وضعیت گونه محصول')
    color = models.ManyToManyField('Color',blank=True,verbose_name='رنگ محصول')
    size = models.ManyToManyField('Size',blank=True,verbose_name='سایز محصول')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE,blank=True,null=True,verbose_name='برند')
    like = models.ManyToManyField(User,blank=True,related_name='product_like',verbose_name='لایک')
    total_like = models.PositiveIntegerField(default=0,verbose_name='مجموع لایک ها')
    unlike = models.ManyToManyField(User,blank=True,related_name='product_unlike',verbose_name='دیس لایک')
    total_unlike = models.PositiveIntegerField(default=0,verbose_name='مجموع دیس لایک ها')
    favourite = models.ManyToManyField(User,blank=True,related_name='fa_user',verbose_name='محصولات محبوب')
    total_favourite = models.PositiveIntegerField(default=0,verbose_name='مجموع محبوب ها')
    sell = models.PositiveIntegerField(default=0,verbose_name='پر فروش')
    view = models.ManyToManyField(User,blank=True,related_name='product_view',verbose_name='بازدید ها')
    num_view = models.PositiveIntegerField(default=0,verbose_name='مجموع بازدید ها')
    
    
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
    
    def jpublish_create(self):
        return jalali_conveter(self.create)
    jpublish_create.short_description = "زمان انتشار دسته بندی "
        

    def category_to_str(self):
        return ", ".join([category.name for category in self.category.active()])
    category_to_str.short_description = "دسته بندی"
    
    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.old_price = self.unit_price


    def save(self,*args,**kwargs):
        if self.old_price != self.unit_price:
            self.update = timezone.now() 
        super().save(*args,**kwargs)
    
    
    def total_like(self):
        return self.like.count()
    
    def total_unlike(self):
        return self.unlike.count()
    
    # Rename model
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        
    
# Size model
class Size(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام سایز')
    
    def __str__(self):
        return self.name
    
    # Rename model
    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایز ها'
        
  
# Color model  
class Color(models.Model):
    color = ColorField(default='#fff',verbose_name='انتخاب رنگ')
    name = models.CharField(max_length=150,verbose_name='نام رنگ')
    
    def __str__(self):
        return self.name
    
    # Rename model
    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'



    # def color_bg(self):
    #     return mark_safe('<div style="background-color:{}"></div>'.format(self.name))
    # color_bg.short_description = 'رنگ'
    # color_bg.allow_tags = True
    


# Variants model
class Variants(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام گونه محصول')
    update = jmodels.jDateTimeField(auto_now=True,verbose_name='زمان بروزرسانی محصول')
    product_variant = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='pr',verbose_name='انتخاب گونه محصول')
    size_variant = models.ForeignKey(Size,on_delete=models.CASCADE,null=True,blank=True,verbose_name='انتخاب سایز محصول')
    color_variant = models.ForeignKey(Color,on_delete=models.CASCADE,null=True,blank=True,verbose_name='انتخاب رنگ محصول')
    amount = models.PositiveIntegerField(verbose_name='تعداد گونه محصول')
    unit_price = models.PositiveIntegerField(verbose_name='قیمت گونه محصول')
    change = models.BooleanField(default=True,verbose_name='عوض کردن')
    discount = models.PositiveIntegerField(null=True,blank=True,verbose_name='در تخفیف گونه محصول')
    total_price = models.PositiveIntegerField(verbose_name='قیمت کل',blank=True, null=True)
    
    
    def __str__(self):
        return self.name
    
    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price   
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.old_price = self.unit_price


    def save(self,*args,**kwargs):
        if self.old_price != self.unit_price:
            self.update = timezone.now() 
        super().save(*args,**kwargs)

    # Rename model
    class Meta:
        verbose_name = 'گونه محصول'
        verbose_name_plural = 'گونه محصولات ' 
    
    
# Model comment 
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='کاربر') 
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='انتخاب محصول') 
    comment = RichTextUploadingField(verbose_name='جزئیات نظر')
    rate = models.PositiveIntegerField(default=1,verbose_name='امتیاز نظر')
    create = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self',related_name='comment_reply',on_delete=models.CASCADE,blank=True, null=True,verbose_name='ریپلای نظر')
    is_reply = models.BooleanField(default=False,verbose_name='آیا ریپلای نظر است ؟')
    comment_like = models.ManyToManyField(User,related_name='com_like',blank=True,verbose_name='لایک نظر')
    total_comment_like = models.PositiveIntegerField(default=0,verbose_name='مجموع لایک های کامنت')
    

    def total_comment_like(self):
        return self.comment_like.count()
    
    def __str__(self):
        return self.product.name
    
    def jpublish(self):
        return jalali_conveter(self.create)
    jpublish.short_description = "زمان نظر"
    
    # Rename model
    class Meta:
        verbose_name = 'نظرات محصول'
        verbose_name_plural = 'نظرات محصولات ' 

# Form comment 
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment','rate']
        
        
# Form Reply for comment
class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
      


# Model Image for product
class Images(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='انتخاب محصول')
    name = models.CharField(max_length=100,blank=True,verbose_name='نام محصول')
    image = models.ImageField(upload_to='images/',blank=True,verbose_name='تصویر محصول')
    
    
    def __str__(self):
        return self.product.name
    
    # Rename model     
    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصولات ' 

# Brand Models
class Brand(models.Model):
    name = models.CharField(max_length=100,blank=True,verbose_name="نام برند")
    image = models.ImageField(upload_to='brand/',blank=True, null=True,verbose_name='تصویر برند ')
    
    def __str__(self):
        return self.name 
    
    #rename model
    class Meta:
        verbose_name = 'برند محصول'
        verbose_name_plural = 'برند محصولات'
        
# Chart models
class Chart(models.Model):
    name = models.CharField(max_length=50,blank=True, null=True,verbose_name='نام محصول')
    unit_price = models.PositiveIntegerField(default=0,verbose_name='قیمت محصول')
    update = jmodels.jDateTimeField(auto_now=True)
    color = models.CharField(max_length=50,blank=True, null=True,verbose_name='رنگ محصول')
    size = models.CharField(max_length=50,blank=True, null=True,verbose_name='سایز محصول')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='pr_update',blank=True, null=True,verbose_name='انتخاب محصول')
    variant = models.ForeignKey(Variants,on_delete=models.CASCADE,related_name='v_update',blank=True, null=True,verbose_name='انتخاب گونه محصول')
    
    def __str__(self):
        return self.name 
    
    #rename model
    class Meta:
        verbose_name = 'چارت محصول'
        verbose_name_plural = 'چارت محصولات'
        
    def save(self,*args,**kwargs):
        old_data_product = Chart.objects.filter(product__exact=self.product,unit_price__exact=self.unit_price)
        old_data_variants = Chart.objects.filter(variant__exact=self.variant,unit_price__exact=self.unit_price)
        if not old_data_product.exists() or not old_data_variants.exists():
            return super(Chart,self).save(*args,**kwargs)
 
        
# Signal for create product models no Variants
def product_post_save(sender,instance,created,*args,**kwargs):
    data = instance
    Chart.objects.create(product=data,unit_price=data.unit_price,update=data.update,name=data.name)
post_save.connect(product_post_save,sender=Product)


# Signal for create product models with Variants
def variant_post_save(sender,instance,created,*args,**kwargs):
    data = instance
    Chart.objects.create(variant=data,unit_price=data.unit_price,update=data.update,name=data.name,size=data.size_variant,color=data.color_variant)
post_save.connect(variant_post_save,sender=Variants)

# Views for product
class Views(models.Model):
    ip = models.CharField(max_length=200,blank=True, null=True,verbose_name='آدرس آی پی کاربر')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True, null=True,verbose_name='بازدید محصول')
    create = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ و زمان بازدید')
    
    
    def __str__(self):
        return self.product.name
    

    #rename model
    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید های محصولات'
        
        
# Gallery for slider in home page
class Gallery(models.Model):
    SALE_OFF = (
        ('بهار','بهار'),
        ('تابستان','تابستان'),
        ('پاییز','پاییز'),
        ('زمستان','زمستان'),
    )
    
    name = models.CharField(max_length=100,blank=True, null=True,verbose_name='متن اسلایدر')
    image = models.ImageField(upload_to='gallery/',blank=True,verbose_name='عکس اسلایدر')
    sale_session = models.CharField(max_length=10,choices=SALE_OFF,blank=True,verbose_name='فروش فصلی')
    sale_off = models.PositiveIntegerField(default=0,blank=True,verbose_name='نخفیف محصول')
    
    
    def __str__(self):
        return self.name
    
    #rename model
    class Meta:
        verbose_name = 'عکس اسلایدر'
        verbose_name_plural = 'عکس های اسلایدر'
        