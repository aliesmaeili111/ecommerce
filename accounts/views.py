from django.shortcuts import render,redirect,reverse,get_object_or_404
from accounts.forms import UserRegisterForm,UserLoginForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from accounts.models import Profile
from accounts.forms import (UserUpdateForm,
                            ProfileUpdateForm,
                            PhoneForm,CodeForm)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from random import randint
from kavenegar import *
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from order.models import ItemOrder
from home.models import Product,Views



class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))
    
email_generator = EmailToken()


# Register View
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data['user_name'],
                                email=data['email'],
                                first_name=data['first_name'],
                                last_name=data['last_name'],
                                password=data['password_2'])
            user.is_active = False
            user.save()
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            url = reverse('accounts:active',kwargs={'uidb64':uidb64,'token':email_generator.make_token(user)})
            link = 'http://' + domain + url
            email = EmailMessage(
                'Active User',
                'hi user pleaze active link  ' + link ,
                'test <aliesmaeili1177@gmail.com>',
                [data['email']]
            )
            email.send(fail_silently=False)
            messages.warning(request,f'User for active email.Pleaze','warning')
            return redirect('home:home')
    else:
        form = UserRegisterForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/register.html',context)


class RegisterEmail(View):
    def get(self,request,uidb64,token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')


# Login View
def user_login(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            remember = data['remember']
            try:
                user = authenticate(request,username=User.objects.get(email=data['user']),password=data['password'])
            except :
                user = authenticate(request,username=data['user'],password=data['password'])
                
            if user is not None:
                login(request,user)
                if not remember:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(86400)
                messages.success(request,f'Welcome {request.user.username}','primary')
                return redirect('home:home')
            else:
                messages.error(request,f'User or password is wrong! {request.user.username}','danger')
                
            
    else:
        login_form = UserLoginForm()
        
    context = {
        'login_form':login_form,
    }
    return render(request,'accounts/login.html',context)

# Logout view
def user_logout(request):
    logout(request)
    messages.success(request,'Your logout','success')
    return redirect('home:home')


# Profile View 
@login_required(login_url='accounts:login')
def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if (user_form.is_valid() and profile_form.is_valid()):
            user_form.save()
            profile_form.save()
            messages.success(request,'Update profile successfuly','success')    
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'profile':profile,
        'user_form':user_form,
        'profile_form':profile_form,
        }
    return render(request,'accounts/profile.html',context)

# Change password view
@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid() :
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,'Change password successfuly','success')
            return redirect('accounts:profile')
        else:
            messages.error(request,'password id Wrong!','danger')
            return redirect('accounts:profile') 
    else:
        form = PasswordChangeForm(request.user)
        context = {
            'form':form,
        }
    return render(request,'accounts/change_password.html',context)


# login phone
def login_phone(request):
    if request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            global random_code,phone
            data = form.cleaned_data
            phone = data['phone']
            random_code = randint(100,10000)
            
            api = KavenegarAPI('546E4F51563753746455367265306D4B5672486B494C467077456B5A6C4932503231675935496B483563673D')
            params = { 'sender' : '', 'receptor': f'0{phone}', 'message' : f'کد ورود به وبسایت{ random_code }'}
            response = api.sms_send( params)
            
            return redirect('accounts:verify')
    else:
        form = PhoneForm()
        
    context = {
        'form':form
    }
    return render(request,'accounts/phone.html',context)

# verify phone code for login
def verify(request):
    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if random_code == data['code'] :
                profile = Profile.objects.get(phone=phone)
                user = User.objects.get(profile__id=profile.id)
                login(request,user)
                messages.success(request,'Welcome user','success')
                return redirect("home:home")
            else:
                messages.error(request,'Wrong your code. Try again',"danger")
      
    else:
        form = CodeForm()
        
    context = {
        'form':form
    }
    return render(request,'accounts/code.html',context)


def favourite(request):
    product = request.user.fa_user.all()
    context = {
        'product':product
    }
    return render(request,'accounts/favourite.html',context)


@login_required(login_url='accounts:login')
def remove_favourite(request,id):
    url = request.META.get("HTTP_REFERER")
    product = get_object_or_404(Product,id=id)
    product.favourite.remove(request.user)
    messages.error(request,'you wishlist remove','danger')
    return redirect(url)
    


def history(request):
    data = ItemOrder.objects.filter(user_id=request.user.id)
    context = {
        'data':data,
    }
    return render(request,'accounts/history.html',context)


def product_view(request):
    product = Views.objects.filter(ip=request.META.get('REMOTE_ADDR')).order_by('-create')[:20]
    context = {
        'product':product,
    }
    return render(request,'accounts/view.html',context)



class ResetPassword(auth_view.PasswordResetView):
    template_name = 'accounts/reset.html'
    success_url = reverse_lazy('accounts:reset_done')
    email_template_name = 'accounts/link.html'
    
    
class DonePassword(auth_view.PasswordResetDoneView):
    template_name='accounts/done.html'
    
    
class ConfirmPassword(auth_view.PasswordResetConfirmView):
    template_name = 'accounts/confirm.html'
    success_url = reverse_lazy('accounts:complete')
    
    
class Complete(auth_view.PasswordResetCompleteView):
    template_name = 'accounts/complete.html'
    
    