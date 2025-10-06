from django.db import models
from utils import UploadFile
from django.utils import timezone
# from django.utils.html import mark_safe
from django.utils.safestring import mark_safe


class Slider(models.Model):
    slider_title1=models.CharField(max_length=500,null=True,blank=True,verbose_name='متن اول')
    slider_title2=models.CharField(max_length=500,null=True,blank=True,verbose_name="متن دوم")
    slider_title3=models.CharField(max_length=500,null=True,blank=True,verbose_name="متن سوم")
    file_upload=UploadFile('images','slider')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر اسلایدر')
    slider_link=models.URLField(max_length=200,null=True,blank=True,verbose_name='لینک')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    published_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
    update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ اخرین بروزرسانی')
    
    def __str__(self):
        return f'{self.slider_title1}'
    
    class Meta:
        verbose_name='اسلاید'
        verbose_name_plural='اسلایدها'
        
    def image_slide(self):
        return mark_safe(f"<img src='/media/{self.image_name}' style='width: 80px; height: 80px;'/>")
    image_slide.short_description='تصویر اسلاید'
    
    def link(self):
        return mark_safe(f"<a href='{self.slider_link}' target='_blank'>link</a>")
    link.short_description='پیوند'