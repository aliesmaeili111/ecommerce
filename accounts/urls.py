from django.urls import path
from accounts.views import (user_register,user_login,
                            user_logout,user_profile,
                            change_password,login_phone,
                            verify,RegisterEmail,
                            ResetPassword,
                            DonePassword,
                            ConfirmPassword,
                            Complete,favourite,history,
                            remove_favourite,product_view)


app_name = 'accounts'

urlpatterns = [
    path('register/',user_register,name='register'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('profile/',user_profile,name='profile'),
    path('change/',change_password,name='change'),
    path('phone/',login_phone,name='phone'),
    path('verify/',verify,name='verify'),
    path('active/<uidb64>/<token>/',RegisterEmail.as_view(),name='active'),
    path('reset/',ResetPassword.as_view(),name='reset'),
    path('reset/done/',DonePassword.as_view(),name='reset_done'),
    path('confirm/<uidb64>/<token>/',ConfirmPassword.as_view(),name='password_reset_confirm'),
    path('complete/done/',Complete.as_view(),name='complete'),
    path('favourite/',favourite,name='favourite'),
    path('favourite/page/<int:page>/',favourite,name='favourite'),
    path('remove_favourite/<int:id>/',remove_favourite,name='remove_favourite'),
    path('history/',history,name='history'),
    path('history/page/<int:page>/',history,name='history'),
    path('view/',product_view,name='product_view'),
    path('view/page/<int:page>/',product_view,name='product_view'),
]
