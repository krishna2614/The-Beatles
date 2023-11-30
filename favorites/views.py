from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import Favorite
import json


def get_user_favorites(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        favorite_restrooms = [favorite.restroom for favorite in favorites]
        return JsonResponse({'favorites': favorite_restrooms})
    return JsonResponse({'favorites': []})


def update_favorite(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        print(data)
        restroom = data['restroom']
        is_favorite = data['favorite']
        from_fav = data['fromFav']

        if is_favorite:
            # Create favorite
            Favorite.objects.create(user=user, restroom=restroom)
        else:
            # Remove from favorites
            if from_fav:
                restroom['isFav'] = True if restroom['isFav'] else False
            else:
                restroom['isFav'] = False if restroom['isFav'] else True
            Favorite.objects.filter(user=user, restroom=restroom).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid request'}, status=400)


def show_page(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        favorite_restrooms = [favorite.restroom for favorite in favorites]

        print(favorite_restrooms)
        return render(request, 'restrooms.html', {'restrooms': favorite_restrooms})
    return redirect('index')
