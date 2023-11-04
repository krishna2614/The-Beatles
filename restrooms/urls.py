from django.urls import path
from .views import index, save_data

urlpatterns = [
    path('', index, name='restrooms'),
    path('savedata/', save_data, name='save_data')
]
