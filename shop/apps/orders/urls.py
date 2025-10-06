from django.urls import path
from .views import *


app_name='orders'
urlpatterns = [    
    path('shop_cart/',ShopCartVeiw.as_view(),name='shop_cart'),
    path('show_shop_cart/',show_shop_cart,name='show_shop_cart'),
    path('add_to_shop_cart/',add_to_shop_cart,name='add_to_shop_cart'),
    path('delete_from_shop_cart/',delete_from_shop_cart,name='delete_from_shop_cart'),
    path('update_shop_cart/',update_shop_cart,name='update_shop_cart'),
    path('status_shop_cart/',status_shop_cart,name='status_shop_cart'),
    path('create_order/<int:order_final_price>/',CreateOrderView.as_view(),name='create_order'),
    path('checkout_order/<int:order_id>/',CheckoutOrderView.as_view(),name='checkout_order'),
    path('applay_coupon/<int:order_id>/',ApplayCoupon.as_view(),name='applay_coupon'),
]