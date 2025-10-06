from django.urls import path
from .views import *


app_name='csf'
urlpatterns = [    
        path('create_comment/<slug:slug>/',CommentView.as_view(),name='create_comment'),
        path('add_score/',add_score,name='add_score'),
        path('add_to_favorites/',add_to_favorites,name='add_to_favorites'),
        path('delete_from_favorite/<int:p_id>',delete_from_favorite,name='delete_from_favorite'),
        path('status_favorites/',status_favorites,name='status_favorites'),
        path('user_favorite/',UserFavoriteView.as_view(),name='user_favorite'),
]