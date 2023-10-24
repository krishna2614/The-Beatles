from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
def index(request):
    # g = GeoIP2()
    # print(g.country('google.com'))
    # print('--------------------------')
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')
    # print(ip)
    # # location = requests.get('https://ipinfo.io/json').json()['loc']
    # # print(location)
    # ip = requests.get('https://api.ipify.org').text
    #
    # # Get the user's location from IPStack
    # location = requests.get('https://ipstack.com/{}/geo'.format(ip)).json()
    # print(location)
    # print(ip_address)
    # print(g.city(ip_address))
    return render(request, 'home.html')


@login_required
def home(request):
    return render(request, 'home.html')