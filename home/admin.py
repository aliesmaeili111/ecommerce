from django.contrib import admin
from home.models import Category,Product,Variants,Size,Color,Comment,Images
import admin_thumbnails


class ProductVariantInlines(admin.TabularInline):
    model = Variants
    extra = 2

@admin_thumbnails.thumbnail('image')
class ImagesInlines(admin.TabularInline):
    model = Images
    extra = 2


# Category admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','create','update','sub_category')
    list_filter = ('name','create','update')
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category,CategoryAdmin)


# Product admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','create','update','amount','available','unit_price','discount','total_price')
    prepopulated_fields = {'slug':('name',)}
    list_filter = ('name','available')
    list_editable = ('amount',)
    inlines = [ProductVariantInlines,ImagesInlines]


admin.site.register(Product,ProductAdmin)

class VariantsAdmin(admin.ModelAdmin):
    list_display = ['name','id']

admin.site.register(Variants,VariantsAdmin)
    
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','id']

admin.site.register(Size,SizeAdmin)

    
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','color']
admin.site.register(Color,ColorAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','create','rate']
admin.site.register(Comment,CommentAdmin)


admin.site.register(Images)