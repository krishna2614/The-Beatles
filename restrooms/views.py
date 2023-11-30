from django.http import JsonResponse
from django.shortcuts import render
from geopy.distance import geodesic
from django.core.paginator import Paginator
import json


def save_data(request):
    request.session['restrooms'] = json.loads(request.body)
    print('Data is stored in the session.')
    return JsonResponse({'status': 'success'})


def index(request):
    if 'restrooms' in request.session:
        restrooms = []
        addressSet = set()
        data = request.session['restrooms']

        for place in data['nearbyRestrooms']:
            origin = (data['currentLocation']['lat'], data['currentLocation']['lng'])
            image_url = place['photoId'] if place['photoId'] else None
            name = place['name']
            address = place['address']
            rating = place['rating'] if place['rating'] else -1
            lat = place['lat']
            lng = place['lng']
            dest = (lat, lng)
            distance = geodesic(origin, dest).miles
            if address in addressSet:
                continue
            restrooms.append({'name': name, 'address': address, 'rating': rating, 'lat': lat, 'lng': lng, 'image_url': image_url, 'distance': distance})
            addressSet.add(address)

        if 'sortby' in request.GET:
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
