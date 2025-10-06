from django.contrib import admin
from .models import *

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display=['image_slide','slider_title1','link','is_active','register_date']
    list_filter=('slider_title1',)
    search_fields=('slider_title1',)
    ordering=('update_date',)
    readonly_fields=('image_slide',)