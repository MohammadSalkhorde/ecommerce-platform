from django import forms
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
#---------------------------------------------------------------------------------
class UserCreationForm(ModelForm):
    password1=forms.CharField(label='رمز عبور',widget=forms.PasswordInput)
    password2=forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput)
    class Meta:
        model=CustomUser
        fields=['mobile_number','email','name','family','gender']
        
    def clean_password2(self):
        pass1=self.cleaned_data['password1']
        pass2=self.cleaned_data['password2']
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن یکسان نیست')
        return pass2
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
#---------------------------------------------------------------------------------
class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField(help_text="برای تغییر رمز عبور روی این <a href='../password'>لینک</a> کلیک کن")
    class Meta:
        model=CustomUser
        fields=['mobile_number','password','email','name','family','gender','is_active','is_admin']
#---------------------------------------------------------------------------------
class RegisterUserForm(ModelForm):
    password1=forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور را وارد کنید','class':'form-control'}))
    password2=forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput(attrs={'placeholder':'تکرار رمز عبور را وارد کنید','class':'form-control'}))
    class Meta:
        model=CustomUser
        fields=['mobile_number']
        widgets={
            'mobile_number':forms.TextInput(attrs={'placeholder':'شماره موبایل را وارد کنید','class':'form-control'}),
        }
        
    def clean_password2(self):
        pass1=self.cleaned_data['password1']
        pass2=self.cleaned_data['password2']
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن یکسان نیست')
        return pass2
#---------------------------------------------------------------------------------
class VerifyRegisterForm(forms.Form):
    active_code=forms.CharField(label='کد فعال سازی', required='لطفا کد فعالسازی را وارد کنید',widget=forms.TextInput(attrs={'placeholder':'کد فعالسازی را وارد کنید','class':'form-control'}))
#---------------------------------------------------------------------------------
class LoginUserForm(forms.Form):
    mobile_number=forms.CharField(label='شماره موبایل', required='لطفا شماره موبایل را وارد کنید',widget=forms.TextInput(attrs={'placeholder':'شماره موبایل را وارد کنید','class':'form-control'}))
    password=forms.CharField(label='رمز عبور', required='لطفا رمز عبور را وارد کنید',widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور را وارد کنید','class':'form-control'}))
#---------------------------------------------------------------------------------
class RememberPasswordForm(forms.Form):
    mobile_number=forms.CharField(label='شماره موبایل', required='لطفا شماره موبایل را وارد کنید',widget=forms.TextInput(attrs={'placeholder':'شماره موبایل را وارد کنید','class':'form-control'}))
#---------------------------------------------------------------------------------
class ChangePasswordForm(forms.Form):
    password1=forms.CharField(label='رمز عبور', required='لطفا رمز عبور را وارد کنید',widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور را وارد کنید','class':'form-control'}))
    password2=forms.CharField(label='تکرار رمز عبور', required='لطفا تکرار رمز عبور را وارد کنید',widget=forms.PasswordInput(attrs={'placeholder':'تکرار رمز عبور را وارد کنید','class':'form-control'}))
    def clean_password2(self):
        pass1=self.cleaned_data['password1']
        pass2=self.cleaned_data['password2']
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن یکسان نیست')
        return pass2
#---------------------------------------------------------------------------------
class UpdateProfileForm(forms.Form):
    mobile_number=forms.CharField(label='',
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل','readonly':'readonly'}))
    name=forms.CharField(label='',
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholdr':'نام خود را وارد کنید'}),
                                  error_messages={'required':'این فیلد نمیتواند خالی باشد'})

    family=forms.CharField(label='',
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خانوادگی خود را وارد کنید'}),
                                  error_messages={'required':'این فیلد نمیتواند خالی باشد'})
    email=forms.CharField(label='',
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'ایمیل خود را وارد کنید'}),
                                  error_messages={'required':'این فیلد نمیتواند خالی باشد'})
    phone_number=forms.CharField(label='',
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'تلفن ثابت خود را وارد کنید'}),
                                  error_messages={'required':'این فیلد نمیتواند خالی باشد'})
    address=forms.CharField(label='',
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'آدرس خود را وارد کنید'}),
                                  error_messages={'required':'این فیلد نمیتواند خالی باشد'})
    image=forms.ImageField(required=False)
#---------------------------------------------------------------------------------
