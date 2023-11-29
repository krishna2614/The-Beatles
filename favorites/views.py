from django.http import JsonResponse
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
        restroom = data['restroom']
        is_favorite = data['favorite']

        if is_favorite:
            # Create favorite
            Favorite.objects.create(user=user, restroom=restroom)
        else:
            # Remove from favorites
            restroom['isFav'] = False if restroom['isFav'] else True
            Favorite.objects.filter(user=user, restroom=restroom).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid request'}, status=400)
