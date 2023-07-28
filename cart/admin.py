from django.contrib import admin
from cart.models import Cart



class CartAdmin(admin.ModelAdmin):
    list_display = ['user','product','variant','quantity']
admin.site.register(Cart,CartAdmin)


# class CompareAdmin(admin.ModelAdmin):
#     list_display = ['user','product','session_key']
# admin.site.register(Compare,CompareAdmin)


