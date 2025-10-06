from django.urls import path
from .views import *


app_name='accounts'
urlpatterns = [    
    path('register/',RegisterUserView.as_view(),name='register'),
    path('verify/',VerifyRegisterView.as_view(),name='vrify'),
    path('login/',LoginUserView.as_view(),name='login'),
    path('logout/',LogoutUserView.as_view(),name='logout'),
    path('panel/',UserPanelView.as_view(),name='panel'),
    path('remember-password/',RememberPasswordView.as_view(),name='remember-password'),
    path('change-password/',ChangePasswordView.as_view(),name='change-password'),
    path('show_last_orders/',show_last_orders,name='show_last_orders'),
    path('update_profile/',UpdateProfileView.as_view(),name='update_profile'),
    path('show_user_payments/',show_user_payments,name='show_user_payments'),
]
