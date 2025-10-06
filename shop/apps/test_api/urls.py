from django.urls import path
from .views import *

app_name='test_api'
urlpatterns = [
    path('products/',AllProductsApi.as_view(),name='products'),
]
