from django.db import models
from utils import UploadFile
from django.utils import timezone
# from ckeditor_uploader.fields import RichTextUploadingFormField
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse
from django.db.models import Sum,Avg
from middlewares.middlewares import RequestMiddleware
#-----------------------------------------------------------------------------------
class Brand(models.Model):
    brand_title=models.CharField(max_length=100,verbose_name='نام برند')
    upload_file=UploadFile('images','brand')
    image_name=models.ImageField(verbose_name='تصویر برند',upload_to=upload_file.upload_to)
    slug=models.SlugField(max_length=200,null=True)
    
    def __str__(self):
        return self.brand_title
    
    class Meta:
        verbose_name='برند'
        verbose_name_plural='برندها'
#-----------------------------------------------------------------------------------
class ProductGroup(models.Model):
    group_title=models.CharField(max_length=100,verbose_name='عنوان گروه کالا')
    upload_file=UploadFile('images','product_group')
    image_name=models.ImageField(verbose_name='تصویر گروه کالا',upload_to=upload_file.upload_to)
    description=models.TextField(verbose_name='توضیحات گروه کالا',null=True,blank=True)
    is_active=models.BooleanField(default=True,blank=True,verbose_name='وضعیت فعال / غیرفعال')
    group_parent=models.ForeignKey('ProductGroup',on_delete=models.CASCADE,verbose_name='والد گروه کالا',blank=True,null=True,related_name='groups')
    slug=models.SlugField(max_length=200,null=True)
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    publish_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ آخرین بروزرسانی')
    
    def __str__(self):
        return self.group_title
    
    class Meta:
        verbose_name='گروه کالا'
        verbose_name_plural='گروه های کالا'
#-----------------------------------------------------------------------------------
class Feature(models.Model):
    feature_name=models.CharField(max_length=100,verbose_name='نام ویژگی')
    product_group=models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='features_of_groups')
    
    def __str__(self):
        return self.feature_name
    
    class Meta:
        verbose_name='ویژگی'
        verbose_name_plural="ویژگی ها"
#-----------------------------------------------------------------------------------
class Product(models.Model):
    product_name=models.CharField(max_length=500,verbose_name='نام کالا')
    # description=models.TextField(null=True,blank=True,verbose_name='توضیحات کالا')
    summery_description=models.TextField(default="",blank=True,null=True)
    description=CKEditor5Field(config_name='default',blank=True)
    upload_file=UploadFile('images','product')
    image_name=models.ImageField(verbose_name='تصویر کالا',upload_to=upload_file.upload_to)
    price=models.PositiveIntegerField(default=0,verbose_name='قیمت کالا')
    product_group=models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='products_of_groups')
    feature=models.ManyToManyField(Feature,through='ProductFeature')
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,related_name='brands')
    is_active=models.BooleanField(default=True,blank=True,verbose_name='وضعیت فعال / غیرفعال')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    published_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ آخرین بروزرسانی')
    slug=models.SlugField(max_length=200,null=True)
    
    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.slug})
    
    def get_price_by_discount(self):
        list1=[]
        for dbd in self.discount_basket_details2.all():
            if (dbd.discount_basket.is_active==True and
                timezone.now() >= dbd.discount_basket.start_date and
                timezone.now() <= dbd.discount_basket.end_date):
                list1.append(dbd.discount_basket.discount)
        discount=0
        if (len(list1)>0):
            discount=max(list1)
        return int(self.price-(self.price*discount/100))
    
    def get_discount_number(self):
        list1=[]
        for dbd in self.discount_basket_details2.all():
            if (dbd.discount_basket.is_active==True and
                timezone.now() >= dbd.discount_basket.start_date and
                timezone.now() <= dbd.discount_basket.end_date):
                list1.append(dbd.discount_basket.discount)
        discount=0
        if (len(list1)>0):
            discount=max(list1)
        return discount
    
    def get_number_in_warehouse(self):
        sum1=self.warehouse_products.filter(warehouse_type_id=1).aggregate(Sum('qty'))
        sum2=self.warehouse_products.filter(warehouse_type_id=2).aggregate(Sum('qty'))
        input=0
        if sum1['qty__sum']!=None:
            input=sum1['qty__sum']
            
        output=0
        if sum2['qty__sum']!=None:
            output=sum2['qty__sum']
            
        return input-output
    
    def get_user_score(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        score=0
        user_score=self.scoring_product.filter(scoring_user=request.user)
        if user_score.count()>0:
            score=user_score[0].score
        return score
    
    def get_average_score(self):
        avgScore=self.scoring_product.all().aggregate(Avg('score'))['score__avg']
        if avgScore==None:
            avgScore=0
        return avgScore
    
    def get_user_favorites(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        user = request.user
        if not user.is_authenticated:
            return False  # چون ناشناس هست
        else:
            flag=self.favorite_product.filter(favorite_user=request.user).exists()
            return flag
    
    def getMainProductGroups(self):
        return self.product_group.all()[0].id
    
    class Meta:
        verbose_name='کالا'
        verbose_name_plural="کالا ها"
#-----------------------------------------------------------------------------------
class FeatureValue(models.Model):
    value_title=models.CharField(max_length=100, verbose_name='عنوان مقدار')
    feature=models.ForeignKey(Feature,on_delete=models.CASCADE, verbose_name='ویژگی',related_name='feature_value')
    
    def __str__(self):
        return f"{self.id} {self.value_title}"
    
    class Meta:
        verbose_name="مقدار ویژگی"
        verbose_name_plural="مقادیر ویژگی ها"
#-----------------------------------------------------------------------------------
class ProductFeature(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='product_features')
    feature=models.ForeignKey(Feature,on_delete=models.CASCADE,verbose_name='ویژگی')
    value=models.CharField(max_length=100,verbose_name='مقدار ویژگی کالا')
    filter_value=models.ForeignKey(FeatureValue,null=True,blank=True,on_delete=models.CASCADE,verbose_name='مقدار ویژگی برای فیلتر')
    
    def __str__(self):
        return f'{self.product} - {self.feature} : {self.value}'
#-----------------------------------------------------------------------------------
class ProductGallery(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='product_gallery')
    upload_file=UploadFile('images','product_gallery')
    image_name=models.ImageField(verbose_name='تصویر کالا',upload_to=upload_file.upload_to)
    
    class Meta:
        verbose_name='تصویر'
        verbose_name_plural="تصاویر"
#-----------------------------------------------------------------------------------