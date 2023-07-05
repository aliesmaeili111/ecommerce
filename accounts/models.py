from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Model Profile
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=250,blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    
# Signal for create model profile
def save_profile_user(sender,**kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance']) 
        profile_user.save()
        
post_save.connect(save_profile_user,sender=User)
