from django.urls import path
from .views import *


app_name='products'
urlpatterns = [    
    path('cheapset_products/',get_cheapset_products,name='cheapset_products'),
    path('last_products/',get_last_products,name='last_products'),
    path('popular_product_groups/',get_popular_product_groups,name='popular_product_groups'),
    path('product_detail/<slug:slug>/',ProductDetailView.as_view(),name='product_detail'),
    path('related_products/<slug:slug>/',get_related_products,name='related_products'),
    path('product_groups/',ProductGroupsView.as_view(),name='product_groups'),
    path('products_by_group/<slug:slug>/',ProductByGroupsView.as_view(),name='products_by_group'),
    path('ajax_admin/',get_filter_value_for_feature,name='ajax_admin'),
    path('products_groups_partial/',get_product_groups,name='products_groups_partial'),
    path('get_brands_patial/<slug:slug>/',get_brands,name='get_brands_patial'),
    path('get_features_for_filter/<slug:slug>/',get_features_for_filter,name='get_features_for_filter'),
    path('compare_list/',ShowCompareView.as_view(),name='compare_list'),
    path('compare_table/',compare_table,name='compare_table'),
    path('add_to_compare_list/',add_to_compare_list,name='add_to_compare_list'),
    path('delete_from_compare_list/',delete_from_compare_list,name='delete_from_compare_list'),
    path('status_of_compare_list/',status_of_compare_list,name='status_of_compare_list'),
    path('get_best_sellers/',get_best_sellers,name='get_best_sellers'),
]