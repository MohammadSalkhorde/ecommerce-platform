from django.shortcuts import render,redirect
from django.views import View
from .forms import *
from utils import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from apps.orders.models import Order
from apps.payments.models import Payment
from django.contrib.auth.decorators import login_required

#--------------------------------------------------------------------------
class RegisterUserView(View):
    def get(self,request,*args,**kwargs):
        form=RegisterUserForm()
        return render(request,'accounts/register.html',{'form':form})
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request,*args,**kwargs):
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            active_code=create_random_code(5)
            CustomUser.objects.create_user(
                mobile_number=data['mobile_number'],
                active_code=active_code,
                password=data['password1']
            )
            request.session['user']={
                'mobile_number':data['mobile_number'],
                'active_code':str(active_code),
                'remember_password':False
            }
            send_sms(mobile=data['mobile_number'],message=f'کد فعالسازی شما {active_code} می باشد.')
            messages.success(request,"کد فعالسازی ارسال شده را وارد کنید",'success')
            return redirect('accounts:vrify')
        messages.error(request,'خطا در انجام ثبت نام','danger')
        return render(request,'accounts/register.html',{'form':form})
#--------------------------------------------------------------------------
class VerifyRegisterView(View):
    def get(self,request):
        form=VerifyRegisterForm()
        return render(request,'accounts/authentication.html',{'form':form})
    
    def post(self,request):
        form=VerifyRegisterForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=request.session['user']
            if data['active_code'] == user['active_code']:
                if user['remember_password'] == False:
                    user=CustomUser.objects.get(mobile_number=user['mobile_number'])
                    user.is_active=True
                    user.active_code=create_random_code(5)
                    user.save()
                    login(request,user)
                    messages.success(request,'ثبت نام با موفقیت انجام شد','success')
                    return redirect('main:index')
                else:
                    messages.success(request,'هویت شما تایید شد، رمز عبور جدید را وارد کنید','success')
                    return redirect('accounts:change-password')
            else:
                messages.error(request,'کد فعالسازی اشتباه است','danger')
                return render(request,'accounts/authentication.html',{'form':form})
        messages.error(request,"اطلاعات وارد شده معتبر نمی باشد",'danger')
        return render(request,'accounts/authentication.html',{'form':form})
#--------------------------------------------------------------------------
class LoginUserView(View):
    def get(self,request):
        form=LoginUserForm()
        return render(request,'accounts/login.html',{'form':form})
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
        
    def post(self,request):
        form=LoginUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(username=data['mobile_number'],password=data['password'])
            if user is not None:
                db_user=CustomUser.objects.get(mobile_number=data['mobile_number'])
                if db_user.is_admin==False:
                    messages.success(request,'ورود با موفقیت انجام شد','success')
                    login(request,user)
                    next=request.GET.get('next')
                    if next is not None:
                        return redirect(next)
                    else:
                        return redirect('main:index')
                else:
                    messages.error(request,'کاربر ادمین نمیتواند از این قسمت وارد شود','danger')
                    return render(request,'accounts/login.html',{'form':form})
            else:
                messages.error(request,"شماره موبایل یا رمز عبور نادرست است",'danger')
                return render(request,'accounts/login.html',{'form':form})
        else:
            messages.error(request,"اطلاعات وارد شده نامعتبر است",'danger')
            return render(request,'accounts/login.html',{'form':form})
#--------------------------------------------------------------------------
class LogoutUserView(View):
    def get(self,request):
        session=request.session.get('shop_cart')
        logout(request)
        request.session['shop_cart']=session
        messages.success(request,'با موفقیت از حساب کاربری خود خارج شدید','success')
        return redirect('main:index')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
#--------------------------------------------------------------------------
class UserPanelView(LoginRequiredMixin,View):
    def get(self,request):
        user=request.user
        try:
            customer=Customer.objects.get(user=request.user)
            user_info={
                'name':user.name,
                'family':user.family,
                'email':user.email,
                'phone_number':customer.phone_number,
                'address':customer.address,
                'image':customer.image_name,
            }
        except ObjectDoesNotExist:
            user_info={
                'name':user.name,
                'family':user.family,
                'email':user.email
            }
            
        return render(request,'accounts/userpanel.html',{'user_info':user_info})
#--------------------------------------------------------------------------
@login_required
def show_last_orders(request):
    orders=Order.objects.filter(customer_id=request.user.id).order_by('-register_date')[:4]
    return render(request,'accounts/partials/show_last_orders.html',{'orders':orders})
#--------------------------------------------------------------------------
class UpdateProfileView(LoginRequiredMixin,View):
    def get(self,request):
        user=request.user
        try:
            customer=Customer.objects.get(user=request.user)
            initial_dict={
                'mobile_number':user.mobile_number,
                'name':user.name,
                'family':user.family,
                'email':user.email,
                'phone_number':customer.phone_number,
                'address':customer.address,
            }
        except ObjectDoesNotExist:
            initial_dict={
                'mobile_number':user.mobile_number,
                'name':user.name,
                'family':user.family,
                'email':user.email,
            }
        form=UpdateProfileForm(initial=initial_dict)
        return render(request,'accounts/update_profile.html',{'form':form,'image':customer.image_name})
    
    def post(self,request):
        form=UpdateProfileForm(request.POST,request.FILES)
        if form.is_valid():
            cd=form.cleaned_data
            user=request.user
            user.name=cd['name']
            user.family=cd['family']
            user.email=cd['email']
            user.save()
            try:
                customer=Customer.objects.get(user=request.user)
                customer.phone_number=cd['phone_number']
                customer.address=cd['address']
                customer.image_name=cd['image']
                customer.save()
            except ObjectDoesNotExist:
                Customer.objects.create(
                    user=request.user,
                    phone_number=cd['phone_number'],
                    address=cd['address'],
                    image_name=cd['image']
                )
            messages.success(request,'ویرایش پروفایل با موفقیت انجام شد')
            return redirect('accounts:panel')
        messages.error(request,'اطلاعات وارد شده معتبر نمی باشد','danger')
        return render(request,'accounts/update_profile.html',{'form':form})
#--------------------------------------------------------------------------
@login_required
def show_user_payments(request):
    payments=Payment.objects.filter(customer_id=request.user.id).order_by('-register_date')
    return render(request,'accounts/show_user_payments.html',{'payments':payments})
#--------------------------------------------------------------------------
class RememberPasswordView(View):
    def get(self,request):
        form=RememberPasswordForm()
        return render(request,'accounts/remember_password.html',{'form':form})
    def post(self,request):
        form=RememberPasswordForm(request.POST)
        try:
            if form.is_valid():
                data=form.cleaned_data
                user=CustomUser.objects.get(mobile_number=data['mobile_number'])
                active_code=create_random_code(5)
                user.active_code=active_code
                user.save()
                send_sms(data['mobile_number'],f'کد تایید حساب کاربری شما {active_code} است.')
                request.session['user']={
                    'mobile_number':data['mobile_number'],
                    'active_code':str(active_code),
                    'remember_password':True
                }
                messages.success(request,'جهت تغییر رمز عبور کد دریافتی را وارد کنید','success')
                return redirect('accounts:vrify')
            else:
                messages.error(request,'اطلاعات وارد شده نامعتبر است','danger')
                return render(request,'accounts/remember_password.html',{'form':form})
        except:
            messages.error(request,"این شماره موبایل وجود ندارد",'danger')
            return render(request,'accounts/remember_password.html',{'form':form})
#--------------------------------------------------------------------------
class ChangePasswordView(View):
    def get(self,request):
        form=ChangePasswordForm()
        return render(request,'accounts/change_password.html',{'form':form})
    def post(self,request):
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session['user']
            user=CustomUser.objects.get(mobile_number=user_session['mobile_number'])
            user.set_password(data['password1'])
            user.active_code=create_random_code(5)
            user.save()
            messages.success(request,"رمز عبور شما با موفقیت تغییر کرد",'success')
            return redirect('accounts:login')
        else:
            messages.error(request,'اطلاعات وارد شده نامعتبر است','danger')
            return render(request,'accounts/change_password.html',{'form':form})
#--------------------------------------------------------------------------
