from django.contrib import admin
from order.models import Order,ItemOrder,Coupon
from django_jalali.admin.filters import JDateFieldListFilter

class ItemInline(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ('user','product','variant','size','color','quantity','price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','email','f_name','l_name','address','jpublish','paid','get_price','code')
    inlines = [ItemInline]
admin.site.register(Order,OrderAdmin)


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code','start','end','discount','active')
    list_filter = (
        ('code',JDateFieldListFilter),
    )
admin.site.register(Coupon,CouponAdmin)


admin.site.register(ItemOrder)
