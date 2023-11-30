from django.urls import path
from . import views

urlpatterns = [
    path('update-favorite/', views.update_favorite, name='update-favorite'),
    path('get-user-favorites/', views.get_user_favorites, name='get-user-favorites'),
    path('favorites/', views.show_page, name='fav_page'),

]
