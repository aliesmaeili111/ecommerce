from django.contrib import admin
from home.models import Category,Product,Variants,Size,Color,Comment,Images,Brand,Chart
import admin_thumbnails


# variant models inline in product model
class ProductVariantInlines(admin.TabularInline):
    model = Variants
    extra = 2

# image inline for product model as Tab
@admin_thumbnails.thumbnail('image')
class ImagesInlines(admin.TabularInline):
    model = Images
    extra = 2


# Category admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','jpublish_create','jpublish_update','sub_category')
    list_filter = ('name','create','update')
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category,CategoryAdmin)


# Product admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category_to_str','jpublish_create','jpublish_update','amount','brand','available','unit_price','discount','total_price')
    prepopulated_fields = {'slug':('name',)}
    list_filter = ('name','available')
    list_editable = ('amount',)
    inlines = [ProductVariantInlines,ImagesInlines]


admin.site.register(Product,ProductAdmin)

# Variants admin
class VariantsAdmin(admin.ModelAdmin):
    list_display = ['name','id']

admin.site.register(Variants,VariantsAdmin)

# Size Admin
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','id']

admin.site.register(Size,SizeAdmin)

# Color Admin
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','color']
admin.site.register(Color,ColorAdmin)

# Comment Admin
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','jpublish','rate']
admin.site.register(Comment,CommentAdmin)

# Image Admin
admin.site.register(Images)

# Brand Admin
admin.site.register(Brand)


# Chart Admin
admin.site.register(Chart)
