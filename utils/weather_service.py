import requests
from config import OPENWEATHER_API_KEY
from datetime import datetime

def get_weather_data(city_name, state=""):
    """Get weather data from OpenWeather API"""
    try:
        if not OPENWEATHER_API_KEY:
            return None, "Please set your OPENWEATHER_API_KEY in the .env file"
        
        # Search query for Indian cities
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
    
    temp = weather_data.get("main", {}).get("temp", 0)
    humidity = weather_data.get("main", {}).get("humidity", 0)
    rainfall = weather_data.get("rain", {}).get("1h", 0) if weather_data.get("rain") else 0
    description = weather_data.get("weather", [{}])[0].get("description", "")
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    
    recommendations = []
    
    # Temperature-based recommendations
    if temp < 15:
        recommendations.append("⚠️ Low temperature detected. Protect crops from frost. Consider covering sensitive crops.")
    elif temp > 35:
        recommendations.append("🔥 High temperature. Ensure adequate irrigation. Mulching can help retain moisture.")
    else:
        recommendations.append("✅ Temperature is suitable for most crops.")
    
    # Humidity-based
    if humidity > 80:
        recommendations.append("💧 High humidity. Watch for fungal diseases. Ensure proper ventilation.")
    elif humidity < 40:
        recommendations.append("🌵 Low humidity. Increase irrigation frequency if needed.")
    
    # Rainfall
    if rainfall > 5:
        recommendations.append("🌧️ Recent rainfall. Ensure proper drainage to prevent waterlogging.")
    
    # Crop-specific recommendations
    crop_recs = get_crop_specific_recommendations(crop_name, temp, humidity, rainfall)
    recommendations.extend(crop_recs)
    
    return "\n".join(recommendations)

def get_crop_specific_recommendations(crop, temp, humidity, rainfall):
    """Crop-specific weather recommendations"""
    recommendations = []
    
    crop_lower = crop.lower()
    
    # Rice
    if "rice" in crop_lower:
        if temp < 20 or temp > 35:
            recommendations.append("Rice prefers 20-35°C. Current temperature may affect growth.")
        if humidity < 60:
            recommendations.append("Rice needs high humidity (60-80%). Consider increasing irrigation.")
    
    # Wheat
    elif "wheat" in crop_lower:
        if temp > 25:
            recommendations.append("Wheat prefers cooler temperatures. High temperature may reduce yield.")
        if rainfall > 10:
            recommendations.append("Excessive rainfall can damage wheat. Ensure field drainage.")
    
    # Tomato
    elif "tomato" in crop_lower:
        if temp > 30:
            recommendations.append("Tomato may experience heat stress. Provide shade if possible.")
        if humidity > 75:
            recommendations.append("High humidity increases risk of blight. Apply preventive fungicides.")
    
    # Potato
    elif "potato" in crop_lower:
        if temp > 25:
            recommendations.append("Potatoes prefer cooler temperatures. Tuber formation may be affected.")
        if humidity > 80:
            recommendations.append("High humidity increases late blight risk.")
    
    # Cotton
    elif "cotton" in crop_lower:
        if temp < 20 or temp > 35:
            recommendations.append("Cotton grows best at 20-35°C.")
        if rainfall > 15:
            recommendations.append("Heavy rainfall can damage cotton bolls. Harvest if ready.")
    
    # Sugarcane
    elif "sugarcane" in crop_lower:
        if temp < 20:
            recommendations.append("Cold weather slows sugarcane growth.")
        if humidity < 50:
            recommendations.append("Sugarcane needs adequate moisture. Increase irrigation.")
    
    # Mango
    elif "mango" in crop_lower:
        if temp < 15:
            recommendations.append("Cold weather may affect mango flowering. Protect trees.")
        if rainfall > 10:
            recommendations.append("Heavy rain during flowering can affect fruit set.")
    
    return recommendations

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

