from django.urls import path
from .views import *


app_name='main'
urlpatterns = [    
    path('',index,name='index'),
    path('sliders/',SliderView.as_view(),name='sliders'),
]