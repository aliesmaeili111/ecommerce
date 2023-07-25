from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


# Manger for model user
# class UserManager(BaseUserManager):
#     def create_user(self,email,username,phone,password):
#         if not email :
#             raise ValueError('plz email')
#         if not username :
#             raise phone('plz username')
#         if not phone :
#             raise ValueError('plz phone')
#         user = self.model(email=self.normalize_email(email),username=username,phone=phone)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self,email,username,phone,password):
#         user = self.create_user(email,username,phone,password)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
        
        
        
# Model User
# class User(AbstractBaseUser):
#     username = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     phone = models.IntegerField()
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username','phone']
    
    
#     objects = UserManager()
    
#     def __str__(self):
#         return self.email
    
#     def has_perm(self,perm,obj=None):
#         return True
    
#     def has_module_perm(self,app_label):
#         return True
    
#     @property
#     def is_staff(self):
#         return self.is_admin
    
    
    
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
