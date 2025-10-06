from django.shortcuts import render
from apps.products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from .Serializers import ProductSerializer
from CustomPermissions import CustomPermissionForProducts

class AllProductsApi(APIView):
    permission_classes=[CustomPermissionForProducts]
    def get(self,request):
        products=Product.objects.filter(is_active=True).order_by('-register_date')
        self.check_object_permissions(request,products)
        ser_date=ProductSerializer(instance=products,many=True)
        return Response(data=ser_date.data)
    