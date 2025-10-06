from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from utils import UploadFile
#---------------------------------------------------------------------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self,mobile_number,email='',name='',family='',active_code=None,gender=None,password=None):
        if not mobile_number:
            raise('لطفا شماره موبایل را وارد کنید')
        
        user=self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self,mobile_number,email,name,family,password=None,active_code=None,gender=None):
        user=self.create_user(
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        
        user.save(using=self._db)
        return user
#---------------------------------------------------------------------------------------
class CustomUser(AbstractBaseUser,PermissionsMixin):
    mobile_number=models.CharField(max_length=11,unique=True,verbose_name='شماره موبایل')
    email=models.EmailField(max_length=200,blank=True,verbose_name='ایمیل')
    name=models.CharField(max_length=50,blank=True,verbose_name='نام')
    family=models.CharField(max_length=50,blank=True,verbose_name='نام خانوادگی')
    GENDER_CHOICES=(('True','مرد'),('False','زن'))
    gender=models.CharField(max_length=50,choices=GENDER_CHOICES,default="True",null=True,blank=True,verbose_name='جنسیت')
    register_date=models.DateField(default=timezone.now,verbose_name="تاریخ ثبت نام")
    active_code=models.CharField(max_length=100,null=True,blank=True,verbose_name='کد فعالسازی')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت فعال/غیرفعال')
    is_admin=models.BooleanField(default=False,verbose_name='ادمین')
    
    objects=CustomUserManager()
    
    USERNAME_FIELD='mobile_number'
    REQUIRED_FIELDS=['email','name','family']
    
    def __str__(self):
        return self.name+' '+self.family
    
    @property
    def is_staff(self):
        return self.is_admin
#---------------------------------------------------------------------------------------
class Customer(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='user',primary_key=True)
    phone_number=models.CharField(max_length=11,null=True,blank=True,verbose_name='تلفن')
    address=models.TextField(null=True,blank=True,verbose_name='آدرس')
    file_upload=UploadFile('images','customer')
    image_name=models.ImageField(upload_to=file_upload.upload_to,null=True,blank=True,verbose_name='عکس پروفایل')
    
    def __str__(self):
        return f'{self.user}'
#---------------------------------------------------------------------------------------