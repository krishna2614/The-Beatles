from django.shortcuts import render
from geopy.distance import geodesic
from django.core.paginator import Paginator
import json

# Create your views here.


def index(request):
    # //https://maps.googleapis.com/maps/api/place/textsearch/json?location=33.25193%2C-97.1576474&query=restrooms&radius=5&key=AIzaSyCxEhJzSEW4WQOINMyTdUblD0w5WRd-n4w


    with open('data.json', 'r') as f:
        data = json.load(f)
        restrooms = []
        addressSet = set()
        for loc in data['results']:
            if loc["formatted_address"] not in list(addressSet):
                origin = (33.25193, -97.1576474)
                dest = (loc['geometry']['location']['lat'], loc['geometry']['location']['lng'])

                if 'photos' not in loc:
                    image_url = None
                    restrooms.append({'name': loc["name"], 'address': loc["formatted_address"], 'rating': loc['rating'],
                                      'lat': loc['geometry']['location']['lat'],
                                      'lng': loc['geometry']['location']['lng'], 'image_url': image_url, 'distance': geodesic(origin, dest).miles})
                else:
                    photo_ref = loc["photos"][0]["photo_reference"]
                    image_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_ref}&key=AIzaSyCxEhJzSEW4WQOINMyTdUblD0w5WRd-n4w'

                    restrooms.append({'name': loc["name"], 'address': loc["formatted_address"], 'rating': loc['rating'], 'lat': loc['geometry']['location']['lat'], 'lng': loc['geometry']['location']['lng'], 'image_url': image_url, 'distance': geodesic(origin, dest).miles})
            addressSet.add(loc["formatted_address"])

    if 'sortby' in request.GET: # or 'sort' in request.GET:
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
        # elif request.GET['sort'] == 'asc':
        #     restrooms = sorted(restrooms, key=lambda d: d['name'])
        # elif request.GET['sort'] == 'dsc':
        #     restrooms = sorted(restrooms, key=lambda d: d['name'], reverse=True)

    # per_page = 3
    # paginator = Paginator(restrooms, per_page)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)
    # if not page_number:
    #     page_number = 1
    # restrooms = paginator.page(page_number)
    return render(request, 'restrooms.html', {'restrooms': restrooms})# 'page_obj': page_obj})
