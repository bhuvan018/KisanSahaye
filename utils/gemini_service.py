import google.generativeai as genai
from config import GEMINI_API_KEY
from PIL import Image
import io


if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def analyze_crop_disease(image, crop_name=""):
    """Analyze crop disease from image using Gemini Vision"""
    try:
        if not GEMINI_API_KEY:
            return "GEMINI_API_KEY missing"
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        
        if isinstance(image, bytes):
            image = Image.open(io.BytesIO(image))
        elif not isinstance(image, Image.Image):
            image = Image.open(image)
        
        prompt = f"""
        Analyze this agricultural image and provide:
        1. Identify any crop disease or pest infestation visible
        2. Describe the symptoms clearly
        3. Provide treatment recommendations in simple Hindi/English for Indian farmers
        4. Suggest organic and chemical treatment options
        5. Preventive measures
        
        {"Crop type: " + crop_name if crop_name else "Try to identify the crop type."}
        
        Respond in simple, accessible language suitable for small-scale Indian farmers.
        """
        
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def analyze_soil_quality(image=None, description=""):
    """Analyze soil quality from image or description"""
    try:
        if not GEMINI_API_KEY:
            return "GEMINI_API_KEY missing"
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        if image:
            vision_model = genai.GenerativeModel('gemini-2.5-flash')
            if isinstance(image, bytes):
                image = Image.open(io.BytesIO(image))
            elif not isinstance(image, Image.Image):
                image = Image.open(image)
            
            prompt = """
            Analyze this soil image and provide:
            1. Visual assessment of soil texture and color
            2. Likely soil type (sandy, clayey, loamy)
            3. Visible organic matter content
            4. Drainage assessment
            5. Recommendations for improvement

            Respond in simple Hindi/English mixed language for Indian farmers.
            """
            response = vision_model.generate_content([prompt, image])
            return response.text
        else:
            prompt = f"""
            Based on this soil description: "{description}"
            Provide:
            1. Soil type assessment
            2. Fertility analysis
            3. Improvement suggestions with organic and chemical options
            4. Suitable crops for this soil type
            5. Nutrient management recommendations
            
            Respond in simple Hindi/English mixed language for Indian farmers.
            """
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        return f"Error analyzing soil: {str(e)}"

def get_crop_recommendations(region, soil_type, preferences=""):
    """Get AI-powered crop diversification recommendations"""
    try:
        if not GEMINI_API_KEY:
            return "Please set your GEMINI_API_KEY in the .env file"
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        As an agricultural expert for Indian farmers, provide crop diversification recommendations:
        
        Region: {region}
        Soil Type: {soil_type}
        Preferences: {preferences if preferences else "None specified"}
        
        Provide:
        1. 3-5 suitable crops for diversification with reasons
        2. Seasonal planting schedule
        3. Market potential and profitability
        4. Risk factors and mitigation
        5. Resource requirements (water, labor, capital)
        6. Intercropping suggestions if applicable
        
        Respond in simple Hindi/English mixed language for small-scale farmers.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting recommendations: {str(e)}"

def get_crop_specific_weather_recommendations(crop_name, weather_data):
    """Get AI-powered crop-specific weather recommendations"""
    try:
        if not GEMINI_API_KEY:
            return "Please set your GEMINI_API_KEY in the .env file"
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        
        temp = weather_data.get("main", {}).get("temp", 0)
        humidity = weather_data.get("main", {}).get("humidity", 0)
        pressure = weather_data.get("main", {}).get("pressure", 0)
        temp_min = weather_data.get("main", {}).get("temp_min", 0)
        temp_max = weather_data.get("main", {}).get("temp_max", 0)
        rainfall = weather_data.get("rain", {}).get("1h", 0) if weather_data.get("rain") else 0
        wind_speed = weather_data.get("wind", {}).get("speed", 0)
        weather_desc = weather_data.get("weather", [{}])[0].get("description", "")
        
        prompt = f"""
        As an agricultural expert for Indian farmers, provide specific weather-based recommendations for {crop_name} crop.
        
        Current Weather Conditions:
        - Temperature: {temp}°C (Range: {temp_min}°C to {temp_max}°C)
        - Humidity: {humidity}%
        - Atmospheric Pressure: {pressure} hPa
        - Weather Description: {weather_desc}
        - Wind Speed: {wind_speed} m/s
        - Recent Rainfall: {rainfall} mm (if applicable)
        
        Provide SPECIFIC recommendations for {crop_name}:
        1. Is current temperature suitable for this crop? If not, what actions to take?
        2. How does current humidity affect this crop? Any disease risks?
        3. Irrigation recommendations based on weather conditions
        4. Any protective measures needed (frost protection, shade, windbreaks, etc.)
        5. Optimal timing for planting/harvesting based on current weather
        6. Disease prevention tips specific to this weather and crop combination
        7. Any immediate actions farmer should take TODAY
        
        Be specific to {crop_name} crop. Don't give generic advice.
        Respond in simple Hindi/English mixed language suitable for small-scale Indian farmers.
        Format as clear, actionable bullet points.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating recommendations: {str(e)}"

def chat_with_ai(question):
    """Conversational AI for farmer queries"""
    try:
        if not GEMINI_API_KEY:
            return "Please set your GEMINI_API_KEY in the .env file"
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        system_prompt = """
        You are a helpful agricultural assistant for Indian farmers. 
        Provide clear, practical advice in simple Hindi/English mixed language.
        Focus on small-scale farming practices, affordable solutions, and local Indian context.
        Be empathetic and supportive.
        """
        
        prompt = f"{system_prompt}\n\nFarmer's Question: {question}\n\nProvide a helpful answer:"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

