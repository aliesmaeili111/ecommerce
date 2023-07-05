from django.contrib import admin
from accounts.models import Profile


# profile admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','phone','address')
    
admin.site.register(Profile,ProfileAdmin)
