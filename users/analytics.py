import requests
from datetime import datetime, timedelta
from django.conf import settings

def get_weather_data(location):
    api_key = settings.OPENWEATHER_API_KEY
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def calculate_yield(weather_data, crop):
    if not weather_data:
        return 0
      
    total_rainfall = sum(entry['rain']['3h'] for entry in weather_data['list'] if 'rain' in entry)
    avg_temperature = sum(entry['main']['temp'] for entry in weather_data['list']) / len(weather_data['list'])
    
    return (crop.farm_size * avg_temperature * total_rainfall) / 1000

def predict_yield(crop):
    weather_data = get_weather_data(crop.user.userprofile.farm_location)
    predicted_yield = calculate_yield(weather_data, crop)
    return f"Predicted yield: {predicted_yield:.2f} kg"
  
def provide_actionable_insights(crop):
    weather_data = get_weather_data(crop.user.userprofile.farm_location)
    predicted_yield = calculate_yield(weather_data, crop)
    
    insights = {
        "predicted_yield": f"{predicted_yield:.2f} kg",
        "recommendations": []
    }

    # Example recommendations based on weather data
    if weather_data:
        avg_temperature = sum(entry['main']['temp'] for entry in weather_data['list']) / len(weather_data['list'])
        total_rainfall = sum(entry['rain']['3h'] for entry in weather_data['list'] if 'rain' in entry)

        if avg_temperature > 30:
            insights["recommendations"].append("Consider increasing irrigation due to high temperatures.")
        if total_rainfall < 50:
            insights["recommendations"].append("Consider additional watering due to low rainfall.")

    return insights
