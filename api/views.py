import requests
from django.http import JsonResponse
import os

def hello_view(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')

    # GET CLIENT'S ORIGINAL IP ADDRESS
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR') # contains IP addresses
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0] # the first being the original client's IP address not the host
    else:
        client_ip = request.META.get('REMOTE_ADDR') # 127.0.0.1 or localhost

    # MAKE API CALLS WITH THE CLIENT'S IP RETRIEVED
    ip_api_key = os.getenv('IPINFO_API_KEY')
    # send request to the api to get response
    ipinfo_url = f'https://ipinfo.io/{client_ip}/json?token={ip_api_key}'
    ip_response = requests.get(ipinfo_url).json()
    # get location
    location = ip_response.get('city', 'Unknown')

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
