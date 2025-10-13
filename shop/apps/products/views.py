from django.shortcuts import render,redirect
from .models import Product,ProductGroup,FeatureValue,Brand
from django.db.models import Q,Count,Min,Max
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from .filters import ProductFilter
from django.core.paginator import Paginator
from .compare import *
#-------------------------------------------------------------------------------
#ارزانترین محصولات
def get_cheapset_products(request ,*args, **kwargs):
    products=Product.objects.filter(is_active=True).order_by('price')[:12]
    product_groups=ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))
    
    context={
        'products':products,
        'product_groups':product_groups
    }
    
    return render(request,'products/partials/cheapset_products.html',context)
#-------------------------------------------------------------------------------

#اخرین محصولات
def get_last_products(request ,*args, **kwargs):
    products=Product.objects.filter(is_active=True).order_by('-published_date')[:5]
    product_groups=ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))
    
    context={
        'products':products,
        'product_groups':product_groups
    }
    
    return render(request,'products/partials/last_products.html',context)

#-------------------------------------------------------------------------------
#دسته های محبوب
def get_popular_product_groups(request):
    product_groups=ProductGroup.objects.filter(Q(is_active=True)).annotate(count=Count('products_of_groups')).order_by('-count')[:6]
    context={
        'product_groups':product_groups
    }
    
    return render(request,'products/partials/popular_product_groups.html',context)
    
#-------------------------------------------------------------------------------
#جزئیات محصول
class ProductDetailView(View):
    def get(self,request,slug):
        product=get_object_or_404(Product,slug=slug)
        if product.is_active:
            return render(request,'products/product_detail.html',{'product':product})

#-------------------------------------------------------------------------------
#محصولات مرتبط
def get_related_products(request ,*args, **kwargs):
    current_product=get_object_or_404(Product,slug=kwargs['slug'])
    related_products=[]
    for group in current_product.product_group.all():
        related_products.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id)))
    return render(request,'products/partials/related_products.html',{'related_products':related_products})

#-------------------------------------------------------------------------------
#لیست تمام گروه های محصولات
class ProductGroupsView(View):
    def get(self,request):
        product_groups=ProductGroup.objects.filter(Q(is_active=True)).annotate(count=Count('products_of_groups')).order_by('-count')
        return render(request,'products/product_groups.html',{'product_groups':product_groups})
    
#-------------------------------------------------------------------------------
#لیست محصولات هر گروه
class ProductByGroupsView(View):
    def get(self,request,*args, **kwargs):
        slug=kwargs['slug']
        current_group=get_object_or_404(ProductGroup,slug=kwargs['slug'])
        products=Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))
        
        res_aggre=products.aggregate(min=Min('price'),max=Max('price'))
        
        #price filter
        filter=ProductFilter(request.GET, queryset=products)
        products=filter.qs
        
        #brand filter
        brands_filter=request.GET.getlist('brand')
        if brands_filter:
            products=products.filter(brand__id__in=brands_filter)
        
        #feature filter
        features_filter=request.GET.getlist('feature')
        if features_filter:
            products=products.filter(product_features__filter_value__id__in=features_filter).distinct()
        
        #sort type
        sort_type=request.GET.get('sort_type')
        if not sort_type:
            sort_type="0"
        if sort_type=="1":
            products=products.order_by('price')
        if sort_type=="2":
            products=products.order_by('-price')
        
        
        group_slug = slug
        product_per_page = 5
        product_count = products.count()

        # مقدار انتخابی کاربر از GET (اگه چیزی نفرسته مقدار پیش‌فرض همون product_per_page باشه)
        show_count = request.GET.get('show_count', product_per_page)
        try:
            show_count = int(show_count)
        except ValueError:
            show_count = product_per_page

        # صفحه‌بندی با تعداد انتخاب‌شده
        paginator = Paginator(products, show_count)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # لیست اعداد برای منوی کشویی
        show_count_product = []
        i = product_per_page
        while i < product_count:
            show_count_product.append(i)
            i *= 2
        show_count_product.append(product_count)

        context = {
            'products': products,
            "current_group": current_group,
            'res_aggre': res_aggre,
            'group_slug': group_slug,
            'page_obj': page_obj,
            'product_count': product_count,
            'filter': filter,
            'sort_type': sort_type,
            'show_count_product': show_count_product,
            'show_count': show_count,   
        }

        return render(request,'products/products_by_group.html',context)
    
    
#-------------------------------------------------------------------------------
#ajax برای پنل ادمین بخش محصولات کالا برای ویژگی
def get_filter_value_for_feature(request):
    if request.method=='GET':
        feature_id = request.GET['feature_id']
        feature_value = FeatureValue.objects.filter(feature_id=feature_id)
        res={fv.value_title:fv.id for fv in feature_value}
        return JsonResponse(data=res,safe=False)
#-------------------------------------------------------------------------------
    
#لیست گروه محصولات برای فیلتر
def get_product_groups(request):
    product_groups=ProductGroup.objects.annotate(count=Count('products_of_groups'))\
        .filter(Q(is_active=True) & ~Q(count=0))\
        .order_by('-count')
        
    return render(request,'products/partials/products_groups.html',{'product_groups':product_groups})

#-------------------------------------------------------------------------------
#لیست برندها برای فیلتر
def get_brands(request, *args, **kwargs):
    product_group=get_object_or_404(ProductGroup, slug=kwargs['slug'])
    brand_list_id=product_group.products_of_groups.filter(is_active=True).values('brand_id')
    brands=Brand.objects.filter(pk__in=brand_list_id)\
        .annotate(count=Count('brands'))\
        .filter(~Q(count=0))\
        .order_by('-count')
        
    return render(request,'products/partials/brands.html',{'brands':brands})

#-------------------------------------------------------------------------------
#لیست های دیگر فیلتر ها بر حسب مقادیر ویژگیهای کالاهای درون گروه
def get_features_for_filter(request,*args, **kwargs):
    product_group=get_object_or_404(ProductGroup,slug=kwargs['slug'])
    feature_list=product_group.features_of_groups.all()
    feature_dict={}
    for feature in feature_list:
        feature_dict[feature]=feature.feature_value.all()
        
    return render(request,'products/partials/features_filter.html',{'feature_dict':feature_dict})
#-------------------------------------------------------------------------------

class ShowCompareView(View):
    def get(self,request,*args, **kwargs):
        compare_list=CompareProduct(request)
        context={
            'compare_list':compare_list
        }
        return render(request,'products/compare_list.html',context)
    
#-------------------------------------------------------------------------------

def compare_table(request):
    compare_list=CompareProduct(request)
    
    products=[]
    for product_id in compare_list.compare_product:
        product=Product.objects.get(id=product_id)
        products.append(product)
     
    features=[]    
    for product in products:
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature)
                
    context={
        'products':products,
        'features':features,
    }
    return render(request,'products/partials/compare_table.html',context)

#-------------------------------------------------------------------------------
def add_to_compare_list(request):
    productId=request.GET.get('productId')
    productGroupId=request.GET.get('productGroupId')
    compareList=CompareProduct(request)
    res=compareList.add_to_compare_product(productId,productGroupId)
    if res == True:
        return HttpResponse('این کالا قبلا به لیست مقایسه اضافه شده.')
    if res != False:
        return HttpResponse('کالا به لیست مقایسه اضافه شد')
    return HttpResponse('فقط میتوانید کالاهایی که همگروهی هستند را به لیست مقایسه اضافه کنید.')
#-------------------------------------------------------------------------------

def delete_from_compare_list(request):
    productId=request.GET.get('productId')
    compareList=CompareProduct(request)
    compareList.delete_from_compare_product(productId)
    return redirect('products:compare_table')

#-------------------------------------------------------------------------------
def status_of_compare_list(request):
    compareList=CompareProduct(request)
    return HttpResponse(compareList.count)

#-------------------------------------------------------------------------------
def get_sell():
    products = Product.objects.all()
    dict1 = {}
    for i in products:
        sell = i.get_sell() or 0  
        dict1[i.id] = sell
    return dict1


#===========================================================================
def get_best_sellers(request, limit=5):
    sell_data = get_sell()  

    sorted_products = sorted(
        ((pid, sell or 0) for pid, sell in sell_data.items()),
        key=lambda x: x[1],
        reverse=True
    )

    top_ids = [pid for pid, _ in sorted_products[:limit]]

    best_sellers = Product.objects.filter(id__in=top_ids)[:6]

    return render(request, 'products/partials/best_sellers.html', {'products': best_sellers})
#===========================================================================
