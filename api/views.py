import requests
from django.conf import settings
from django.http import JsonResponse
import os

def hello_view(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')

    # GET IP 
    ip_api_key = os.getenv('IPINFO_API_KEY')
    # send request to the api to get response
    ipinfo_url = f'https://ipinfo.io/json?token={ip_api_key}'
    ip_response = requests.get(ipinfo_url).json()
    if settings.DEBUG: # for localhost
        client_ip = request.META.get('REMOTE_ADDR')
    else:
        client_ip = ip_response.get('ip')
    # get location
    location = ip_response.get('city')

    # GET TEMPERATURE
    openweather_api_key = os.getenv('OPENWEATHERAPI_API_KEY')
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={openweather_api_key}'
    temp_response = requests.get(weather_url).json()
    temperature = temp_response.get('main').get('temp')

    response = {
        'client_ip': client_ip,
        'location': location,
        'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees in {location}'
    }

    return JsonResponse(response)
