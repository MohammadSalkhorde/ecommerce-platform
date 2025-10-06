from django.contrib import admin
from .models import *
from django.db.models.aggregates import Count
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description,order_field
#==========================================================
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display=('brand_title',)
    list_filter=('brand_title',)
    search_fields=('brand_title',)
    ordering=('brand_title',)
#==========================================================

def de_active_product_group(modeladmin,request,queryset):
    res=queryset.update(is_active=False)
    message=f' تعداد گروه {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)
    #----------------------------------------------------
def active_product_group(modeladmin,request,queryset):
    res=queryset.update(is_active=True)
    message=f'تعداد گروه {res} کالا فعال شد'
    modeladmin.message_user(request,message)
    #----------------------------------------------------
def export_json(modeladmin,request,queryset):
    res=HttpResponse(content_type='application/json')
    serializers.serialize('json',queryset,stream=res)
    return res
    #----------------------------------------------------
class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model=ProductGroup
    #----------------------------------------------------
class GroupFilter(SimpleListFilter):
    title='گروه محصولات'
    parameter_name='group'
    
    def lookups(self, request, model_admin):
        sub_group=ProductGroup.objects.filter(~Q(group_parent=None))
        groups=[item.group_parent for item in sub_group]
        return [(item.id, item.group_title) for item in groups]
    #--------------------------------------------
    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(Q(group_parent=self.value()))
        return queryset
    #----------------------------------------------------
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display=('group_title','is_active','group_parent','slug','register_date','update_date','count_sub_group')
    list_filter=(('group_title',DropdownFilter),('group_parent',DropdownFilter))
    search_fields=('group_title',)
    ordering=('group_parent','group_title')
    inlines=[ProductGroupInstanceInlineAdmin]
    actions=[de_active_product_group,active_product_group,export_json]
    
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductGroupAdmin,self).get_queryset(*args, **kwargs)
        qs = qs.annotate(sub_group=Count('groups'))
        qs = qs.annotate(sub_group=Count('products_of_groups'))
        return qs
    
    def count_sub_group(self,obj):
        return obj.sub_group
    
    def count_products_of_groups(self,obj):
        return obj.products_of_groups
    
    count_sub_group.short_description='تعداد زیر گروه ها'
    de_active_product_group.short_description='غیرفعال کردن گروه های انتخاب شده'
    active_product_group.short_description='فعال کردن گروه های انتخاب شده'
    count_products_of_groups.short_description='تعداد کالاهای گروه'
#==========================================================

def de_active_product(modeladmin,request,queryset):
    res=queryset.update(is_active=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)
    #----------------------------------------------------
def active_product(modeladmin,request,queryset):
    res=queryset.update(is_active=True)
    message=f'تعداد {res} کالا فعال شد'
    modeladmin.message_user(request,message)
    #----------------------------------------------------
class ProductFeatureInlineAdmin(admin.TabularInline):
    model = ProductFeature
    extra=3
    
    class Media:
        js=(
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_scripts.js'
            )
    #----------------------------------------------------
class ProductGalleryInlineAdmin(admin.TabularInline):
    model = ProductGallery
    extra = 3
    #----------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','brand','is_active','update_date','slug','display_product_group')
    list_filter=('brand','product_group')
    search_fields=('product_group',)
    ordering=('update_date','product_name')
    actions=[active_product,de_active_product,]
    inlines=[ProductFeatureInlineAdmin,ProductGalleryInlineAdmin,]
    list_editable=['is_active']
    
    def display_product_group(self,obj):
        return ', '.join([i.group_title for i in obj.product_group.all()])
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name=='product_group':
            kwargs["queryset"]=ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    display_product_group.short_description='گروه های کالا'
    de_active_product.short_description='غیرفعال کردن گروه های انتخاب شده'
    active_product.short_description='فعال کردن گروه های انتخاب شده'
#==========================================================
class FeatureValueInline(admin.TabularInline):
    model=FeatureValue
    extra=3
    #----------------------------------------------------
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display=('feature_name','display_groups','display_feature_values')
    list_filter=('feature_name',)
    search_fields=('feature_name',)
    ordering=('feature_name',)
    inlines=[FeatureValueInline,]
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            kwargs['queryset'] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def display_groups(self,obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])
    
    def display_feature_values(self,obj):
        return ', '.join([feature_value.value_title for feature_value in obj.feature_value.all()])
    
    display_groups.short_description='گروه های دارای این ویژگی'
    display_feature_values.short_description='مقادیر ممکن برای این ویژگی'
#==========================================================