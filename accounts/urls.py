from django.urls import path
from accounts.views import (user_register,user_login,
                            user_logout,user_profile,
                            change_password,login_phone,
                            verify)


app_name = 'accounts'

urlpatterns = [
    path('register/',user_register,name='register'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('profile/',user_profile,name='profile'),
    path('change/',change_password,name='change'),
    path('phone/',login_phone,name='phone'),
    path('verify/',verify,name='verify'),
]
