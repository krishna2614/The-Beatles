from django.urls import path
from . import views

urlpatterns = [
    path('store-search-query/', views.store_search_query, name='store_search_query'),
    path('get-search-history/', views.get_search_history, name='get_search_history'),
]
