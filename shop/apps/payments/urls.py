from django.urls import path
from .views import *


app_name='payments'
urlpatterns = [    
    path('zarinpal_payment/<int:order_id>/',ZarinpalPaymentView.as_view(),name='zarinpal_payment'),
    path('verify/',ZarinpalPaymentVerifayView.as_view(),name='zarinpal_payment_verifay'),
    path('show_verifay_message/<str:message>/',show_verifay_message,name='show_verifay_message'),
]