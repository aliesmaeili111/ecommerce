from django.contrib import admin
from order.models import Order,ItemOrder,Coupon


class ItemInline(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ('user','product','variant','size','color','quantity','price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','email','f_name','l_name','address','create','paid','get_price')
    inlines = [ItemInline]
admin.site.register(Order,OrderAdmin)


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code','start','end','discount','active')
admin.site.register(Coupon,CouponAdmin)

admin.site.register(ItemOrder)