from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile

# error form accounts(login,register)
error = {
    'min_length' : 'حداقل باید 5 حرف باشد',
    'required' : ' این فیلد اجباری است',
    'invalid':'لطفا یک ایمیل معتبر وارد کنید',
    'exists':'لطفا یک ایمیل معتبر وارد کنید',
}

# Register form
class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=50,error_messages=error,widget=forms.TextInput(attrs={'placeholder':'plz username'}))
    email =  forms.EmailField(error_messages=error,widget=forms.TextInput(attrs={'placeholder':'plz email'}))
    first_name = forms.CharField(max_length=50,error_messages=error,min_length=5,widget=forms.TextInput(attrs={'placeholder':'plz first name'}))
    last_name = forms.CharField(max_length=50,error_messages=error,min_length=5,widget=forms.TextInput(attrs={'placeholder':'plz last name'}))
    password_1 = forms.CharField(max_length=50,error_messages=error,min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'plz password'}))
    password_2 = forms.CharField(max_length=50,error_messages=error,min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'plz Confirm password'}))
    
    
    def clean_user_name(self):
        user = self.cleaned_data["user_name"]
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('User exists')
        return user
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email exists')
        return email
    
    def clean_password_2(self):
        password_1 = self.cleaned_data["password_1"]
        password_2 = self.cleaned_data["password_2"]
        if password_1 != password_2:
            raise forms.ValidationError('password not match')
        
        elif len(password_2) <= 8 :
            raise forms.ValidationError('password to short')
            
        elif not any(x.isupper() for x in password_2):
            raise forms.ValidationError('باید پسورد شما حداقل یک حروف بزرگ داشته باشد')
        return password_1
    
    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if len(first_name) > 50:
            raise forms.ValidationError('اسم شما طولانی است')
        return first_name
        
    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if len(last_name) > 50:
            raise forms.ValidationError('نام خانوادگی شما طولانی است')
        return last_name
    
# Login form    
class UserLoginForm(forms.Form):
    user = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    
# User Update form
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        
# Profile Update form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone','address']
        
        
# Login with mobile 
class PhoneForm(forms.Form):
    phone = forms.IntegerField()
    
    
# Verify code with mobile 
class CodeForm(forms.Form):
    code = forms.IntegerField()