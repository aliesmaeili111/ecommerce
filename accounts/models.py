from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Model Profile
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='کاربر')
    phone = models.IntegerField(blank=True, null=True,verbose_name='شماره تلفن')
    address = models.CharField(max_length=250,blank=True, null=True,verbose_name='آدرس')
    profile_image = models.ImageField(upload_to='profile/',default='user.png',blank=True, null=True,verbose_name='تصویر پروفایل')
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'
    
    
# Signal for create model profile
def save_profile_user(sender,**kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance']) 
        profile_user.save()
        
post_save.connect(save_profile_user,sender=User)
