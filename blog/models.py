from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator,MinValueValidator,MaxLengthValidator
from extensions.utils import jalali_conveter
from django.utils.html import format_html
from taggit.managers import TaggableManager
from django_jalali.db import models as jmodels


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')
    
    
class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)
    

class Category(models.Model):
    parent = models.ForeignKey('self',verbose_name='زیر دسته بندی',default=None,related_name='children',on_delete=models.SET_NULL,blank=True,null=True)
    title = models.CharField(max_length = 200,verbose_name='عنوان دسته بندی',validators = [MaxLengthValidator(200,'لطفا بین 1 تا 200 حرف بنوسید')],help_text="از 1 تا 200 حرف بنویسید")
    slug = models.SlugField(max_length = 30,unique = True,allow_unicode=True,verbose_name='آدرس دسته بندی',validators = [MaxLengthValidator(30,'لطفا بین 1 تا 30 حرف بنوسید')],help_text="از 1 تا 30 حرف بنویسید")
    status = models.BooleanField(default=True,verbose_name="نمایش دادن",help_text="آیا نمایش داده شود ؟")
    created = models.DateTimeField(auto_now_add = True)
    position = models.IntegerField(default=1000,validators=[MinValueValidator(1000),MaxValueValidator(1000000000)],unique=True,verbose_name="موقعیت")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['parent__id','created']         
        
        
    def __str__(self):
        return self.title

    objects = CategoryManager()

class Article(models.Model):
    
    STATUS_CHOICES = (
        ('d','پیش نویس'),
        ('p','منتشر شده')
    )
    
    author = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name="articles",verbose_name="نویسنده",help_text="یک نویسنده کارمندی را انتخاب کنید")
    title = models.CharField(max_length = 250,verbose_name='عنوان مقاله',help_text = 'لطفا بیشتر از 250 حرف ننویسید',validators=[MaxLengthValidator(250,"لطفا بین 1 تا 250 حرف بنویسید")])
    slug = models.SlugField(max_length = 35,allow_unicode=True,unique = True,verbose_name='آدرس مقاله',help_text = 'لطفا بیشتر از 35 حرف ننویسید',validators=[MaxLengthValidator(35,"لطفا بین 1 تا 35 حرف بنویسید")])
    category = models.ManyToManyField(Category,verbose_name="دسته بندی",related_name="articles",help_text="کنترل یا فرمان را در مک نگه دارید تا بیش از یک مورد انتخاب شود|")
    description = RichTextField(verbose_name="محتوای مقاله",help_text="محتوایی برای مقاله خود بنویسید")
    thumbnail = models.ImageField(upload_to='images_blog',verbose_name="تصویر مقاله",help_text='برای مقاله تصویری انتخاب کنید')
    publish = jmodels.jDateTimeField(default = timezone.now,verbose_name='زمان انتشار',help_text = 'فرمت صحیح تاریخ YYYY-MM-DD')
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 1,choices = STATUS_CHOICES,verbose_name='وضعیت',help_text="وضعیت مقاله را انتخاب کنید")
    tag = TaggableManager(blank=True)
    likes = models.ManyToManyField(User,related_name='likes',verbose_name='لایک')
   
    
    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']
   
    def jpublish(self):
        return jalali_conveter(self.publish)
    jpublish.short_description = 'تاریخ انتشار'
    
    def thumbnail_tag(self):
        return format_html("<img src='{}' width=70px hieght=30px style='border-radius:8px'; >".format(self.thumbnail.url))
    thumbnail_tag.short_description = "تصویر مقاله"

    def __str__(self):
        return self.title
    
    objects = ArticleManager()

class Comment(models.Model):
    comment = RichTextField(verbose_name='نظر',help_text="نظر خود را بنویسید")
    user = models.ForeignKey(User,related_name='user_comment',on_delete=models.SET_NULL,null=True,verbose_name='کاربر')
    active = models.BooleanField(default=False,verbose_name='فعال')
    article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name='مقاله')
    date = jmodels.jDateTimeField(auto_now_add=True,verbose_name='زمان انتشار',help_text = 'فرمت صحیح تاریخ YYYY-MM-DD')
    likes = models.ManyToManyField(User,related_name='likes_comment',verbose_name='لایک')
   

    def __str__(self):
        return self.comment[:12]
    
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ['-date']
