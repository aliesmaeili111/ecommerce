from django.contrib import admin
from blog.models import Article,Category
from django.contrib.auth.models import User
from django.utils.html import format_html
from django_jalali.admin.filters import JDateFieldListFilter


def make_published(modeladmin,request,queryset):
    
    rows_updated = queryset.update(status="p")
    if rows_updated == 1 :
        message_bit = ' منتشر شد.'
    else:
        message_bit = ' منتشر شدند'
    modeladmin.message_user(request,f"{rows_updated}مقاله {message_bit}")
    
make_published.short_description ="انتشار مقالات انتخاب شده"

    
def make_draft(modeladmin,request,queryset):
    
    rows_updated = queryset.update(status="d")
    if rows_updated == 1 :
        message_bit = ' پیش نویس شد.'
    else:
        message_bit = ' پیش نویس شدند'
    modeladmin.message_user(request,f"{rows_updated}مقاله {message_bit}") 
    
make_draft.short_description ="پیش نویس شدن مقالات انتخاب شده"    

def make_active(modeladmin,request,queryset):
    
    rows_updated = queryset.update(status=True)
    if rows_updated == 1 :
        message_bit = ' نمایش داده شد.'
    else:
        message_bit = ' نمایش داده شدند'
    modeladmin.message_user(request,f"{rows_updated}دسته بندی {message_bit}")
    
make_active.short_description ="نمایش دسته بندی انتخاب شده"

def make_not_active(modeladmin,request,queryset):
    
    rows_updated = queryset.update(status=False)
    if rows_updated == 1 :
        message_bit = ' نمایش داده نمیشه.'
    else:
        message_bit = ' نمایش داده نمیشوند'
    modeladmin.message_user(request,f"{rows_updated}دسته بندی {message_bit}")
    
make_not_active.short_description =" لغو نمایش دسته بندی انتخاب شده"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self,db_field,request,**kwargs):
        if db_field.name == 'author':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super(ArticleAdmin,self).formfield_for_foreignkey(db_field,request,**kwargs)
    
    list_display = ('name_colored','slug','thumbnail_tag','author_name','category_to_str','publish','status')
    list_display_links = ('name_colored','slug')
    list_filter = ('publish','status','author')
    list_editable = ('status',)
    search_fields =  ['title','slug']
    prepopulated_fields = {'slug':('title',)} 
    list_per_page = 15
    date_hierarchy = 'publish'
    ordering = ['-status','-publish']
    actions = [make_published,make_draft]

    def name_colored(self,obj):
        if obj.status == 'p':
            color_code = '0109FF'
        else:
            color_code = 'FF0000'
        html ="<span style='color:#{}'>{}</span>".format(color_code,obj.title[:30])
        return format_html(html)
    name_colored.short_description = 'عنوان مقاله'

    def category_to_str(self,obj):
        return ", ".join([category.title for category in obj.category.active()])
    category_to_str.short_description = "دسته بندی"

    def author_name(self,obj):
        return obj.author.profile.first_name +' '+ obj.author.profile.last_name
    author_name.short_description = "نویسنده"


@admin.register(Category)  
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ('title','slug','parent','status')
    list_display_links = ('title','slug')
    list_filter = (['status',])
    list_editable = ('status',)
    search_fields =  ('title','slug','position')
    prepopulated_fields = {'slug':('title',)}
    list_per_page = 10
    actions = [make_active,make_not_active]
