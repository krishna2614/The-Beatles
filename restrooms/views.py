from django.http import JsonResponse
from django.shortcuts import render, redirect
from geopy.distance import geodesic
from django.core.paginator import Paginator
import json


def save_data(request):
    request.session['restrooms'] = json.loads(request.body)
    print('Data is stored in the session.')
    return JsonResponse({'status': 'success'})


def index(request):
    # del request.session['restrooms']
    if 'restrooms' in request.session:
        restrooms = []
        data = request.session['restrooms']

        print(data['nearbyRestrooms'][0])
        # return JsonResponse({'status': 'success', 'data': data})
        for place in data['nearbyRestrooms']:
            origin = (data['currentLocation']['lat'], data['currentLocation']['lng'])
            image_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={place["placeId"]}&key=AIzaSyCxEhJzSEW4WQOINMyTdUblD0w5WRd-n4w' if place['placeId'] else None
            name = place['name']
            address = place['address']
            rating = place['rating'] if place['rating'] else -1
            lat = place['lat']
            lng = place['lng']
            dest = (lat, lng)
            distance = geodesic(origin, dest).miles

            restrooms.append({'name': name, 'address': address, 'rating': rating, 'lat': lat, 'lng': lng, 'distance': distance})

        if 'sortby' in request.GET:  # or 'sort' in request.GET:
            if request.GET.get('sortby') == 'rating':
                sort = request.GET.get('sort')
                if sort == 'asc':
                    restrooms = sorted(restrooms, key=lambda d: d['rating'])
                else:
                    restrooms = sorted(restrooms, key=lambda d: d['rating'], reverse=True)
            elif request.GET.get('sortby') == 'distance':
                sort = request.GET.get('sort')
                if sort == 'asc':
                    restrooms = sorted(restrooms, key=lambda d: d['distance'])
                else:
                    restrooms = sorted(restrooms, key=lambda d: d['distance'], reverse=True)

        per_page = 3
        paginator = Paginator(restrooms, per_page)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        if not page_number:
            page_number = 1
        restrooms = paginator.page(page_number)
        return render(request, 'restrooms.html', {'restrooms': restrooms, 'page_obj': page_obj})
    else:
        return render(request, 'restrooms.html')
