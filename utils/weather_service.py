import requests
from config import OPENWEATHER_API_KEY
from datetime import datetime


try:
    from utils.gemini_service import get_crop_specific_weather_recommendations
except ImportError:
    
    from gemini_service import get_crop_specific_weather_recommendations

def get_weather_data(city_name, state=""):
    """Get weather data from OpenWeather API"""
    try:
        if not OPENWEATHER_API_KEY:
            return None, "Please set your OPENWEATHER_API_KEY in the .env file"
        
        
        query = f"{city_name}, {state}, India" if state else f"{city_name}, India"
        
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": query,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data, None
        else:
            return None, f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"Error fetching weather: {str(e)}"

def get_weather_recommendations(crop_name, weather_data):
    """Generate weather-based recommendations for crops"""
    if not weather_data:
        return "Weather data not available"
    
    
    if crop_name:
        try:
            return get_crop_specific_weather_recommendations(crop_name, weather_data)
        except Exception as e:
            
            return f"Error getting AI recommendations: {str(e)}\n\n{get_generic_weather_recommendations(weather_data)}"
    
    
    return get_generic_weather_recommendations(weather_data)

def get_generic_weather_recommendations(weather_data):
    """Generate generic weather-based recommendations"""
    temp = weather_data.get("main", {}).get("temp", 0)
    humidity = weather_data.get("main", {}).get("humidity", 0)
    rainfall = weather_data.get("rain", {}).get("1h", 0) if weather_data.get("rain") else 0
    description = weather_data.get("weather", [{}])[0].get("description", "")
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    
    recommendations = []
    
    
    if temp < 15:
        recommendations.append("⚠️ Low temperature detected. Protect crops from frost. Consider covering sensitive crops.")
    elif temp > 35:
        recommendations.append("🔥 High temperature. Ensure adequate irrigation. Mulching can help retain moisture.")
    else:
        recommendations.append("✅ Temperature is suitable for most crops.")
    
    
    if humidity > 80:
        recommendations.append("💧 High humidity. Watch for fungal diseases. Ensure proper ventilation.")
    elif humidity < 40:
        recommendations.append("🌵 Low humidity. Increase irrigation frequency if needed.")
    
    
    if rainfall > 5:
        recommendations.append("🌧️ Recent rainfall. Ensure proper drainage to prevent waterlogging.")
    
    recommendations.append("\n💡 Tip: Select a specific crop to get personalized recommendations!")
    
    return "\n".join(recommendations)

def format_weather_info(weather_data):
    """Format weather data for display"""
    if not weather_data:
        return "Weather data not available"
    
    main = weather_data.get("main", {})
    weather = weather_data.get("weather", [{}])[0]
    wind = weather_data.get("wind", {})
    
    info = f"""
    **Current Weather:**
    - Temperature: {main.get('temp', 'N/A')}°C (Feels like: {main.get('feels_like', 'N/A')}°C)
    - Humidity: {main.get('humidity', 'N/A')}%
    - Pressure: {main.get('pressure', 'N/A')} hPa
    - Weather: {weather.get('description', 'N/A').title()}
    - Wind Speed: {wind.get('speed', 'N/A')} m/s
    
    **Temperature Range:**
    - Min: {main.get('temp_min', 'N/A')}°C
    - Max: {main.get('temp_max', 'N/A')}°C
    """
    
    return info

