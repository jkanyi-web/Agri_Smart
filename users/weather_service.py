import requests
from django.conf import settings

def get_weather_data(location):
    api_key = settings.OPENWEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None
