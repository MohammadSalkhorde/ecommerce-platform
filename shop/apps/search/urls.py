from django.urls import path
from .views import *


app_name='search'
urlpatterns = [    
   path('',SearchResualtsView.as_view(),name='search_view'),
]