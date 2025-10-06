from django.shortcuts import render,redirect
from django.db.models import Q
from apps.products.models import Product
from django.views import View

class SearchResualtsView(View):
    def get(self,request,*args, **kwargs):
        query=self.request.GET.get('q')
        products=Product.objects.filter(Q(product_name__icontains=query) | Q(description__icontains=query))
        
        context={
            'products':products
        }
        
        return render(request,'search/search_resualt.html',context)