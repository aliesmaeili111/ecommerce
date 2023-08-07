from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

# from django.contrib.auth.forms import ReadOnlyPasswordHashField



# class UserCreateForm(forms.ModelForm):
#     password_1 = forms.CharField(widget=forms.PasswordInput)
#     password_2 = forms.CharField(widget=forms.PasswordInput)
    
#     class Meta:
#         model = User
#         fields = ['email','username','phone']
        
#     def clean_password_2(self):
#         data = self.cleaned_data
#         if data['password_2'] and data['password_1'] and data['password_2'] != data['password_1']:
#             raise forms.ValidationError('plz check')

#         return data['password_2']
    
#     def save(self,commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password_2'])
#         if commit:
#             user.save()
#         return user
    

# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField
    
#     class Meta:
#         model = User
#         fields = ['email','username','phone']
        
#     def clean_password(self):
#         return self.initial['password']
    

    
# error form accounts(login,register)
error = {
    'min_length' : 'حداقل باید 5 حرف باشد',
    'required' : ' این فیلد اجباری است',
    'invalid':'لطفا یک ایمیل معتبر وارد کنید',
    'exists':'لطفا یک ایمیل معتبر وارد کنید',
}

# Register form
class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=50,error_messages=error,widget=forms.TextInput(attrs={'placeholder':'نام کاربری'}))
    email =  forms.EmailField(error_messages=error,widget=forms.TextInput(attrs={'placeholder':'ایمیل'}))
    first_name = forms.CharField(max_length=50,error_messages=error,min_length=3,widget=forms.TextInput(attrs={'placeholder':'نام'}))
    last_name = forms.CharField(max_length=50,error_messages=error,min_length=5,widget=forms.TextInput(attrs={'placeholder':'نام خانوادگی'}))
    password_1 = forms.CharField(max_length=50,error_messages=error,min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور','id':'password'}))
    password_2 = forms.CharField(max_length=50,error_messages=error,min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'تایید رمز عبور'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
    def clean_user_name(self):
        user = self.cleaned_data["user_name"]
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('این نام کاربری از قبل وجود دارد')
        return user
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل از قبل وجود دارد')
        return email
    
    def clean_password_2(self):
        password_1 = self.cleaned_data["password_1"]
        password_2 = self.cleaned_data["password_2"]
        if password_1 != password_2:
            raise forms.ValidationError('رمز عبور با تایید آن مطابقت ندارد')
        
        elif len(password_2) <= 8 :
            raise forms.ValidationError('رمز عبور شما خیلی ضعیف است')
            
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
    user = forms.CharField(max_length=50,min_length=3)
    password = forms.CharField(max_length=50)
    remember = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean_user(self):
        user = self.cleaned_data["user"]
        if not User.objects.filter(username=user).exists() :
            raise forms.ValidationError('این کاربر در فروشگاه ما وجود ندارد')
        return user
    
# User Update form
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        
# Profile Update form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone','address','profile_image']
        
        
# Login with mobile 
class PhoneForm(forms.Form):
    phone = forms.IntegerField()
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
    
# Verify code with mobile 
class CodeForm(forms.Form):
    code = forms.IntegerField()