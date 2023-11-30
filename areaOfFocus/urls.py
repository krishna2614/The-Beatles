from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='area_of_focus'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
