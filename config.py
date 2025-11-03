import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# Indian crop categories
CEREALS = ["Rice", "Wheat", "Maize", "Bajra", "Jowar", "Ragi"]
PULSES = ["Chickpea", "Pigeon Pea", "Lentils", "Moong", "Urad", "Black Gram"]
OILSEEDS = ["Groundnut", "Mustard", "Soybean", "Sunflower", "Sesame"]
CASH_CROPS = ["Cotton", "Sugarcane", "Jute", "Tobacco"]
VEGETABLES = ["Tomato", "Onion", "Potato", "Cabbage", "Cauliflower", "Brinjal", "Okra"]
FRUITS = ["Mango", "Banana", "Citrus", "Grapes", "Pomegranate", "Guava"]
SPICES = ["Turmeric", "Chili", "Coriander", "Cumin", "Cardamom", "Black Pepper"]

ALL_CROPS = CEREALS + PULSES + OILSEEDS + CASH_CROPS + VEGETABLES + FRUITS + SPICES

# Indian states with major agricultural regions
INDIAN_STATES = [
    "Punjab", "Haryana", "Uttar Pradesh", "Bihar", "West Bengal",
    "Maharashtra", "Gujarat", "Rajasthan", "Madhya Pradesh", "Karnataka",
    "Andhra Pradesh", "Tamil Nadu", "Kerala", "Odisha", "Assam",
    "Jharkhand", "Chhattisgarh", "Himachal Pradesh", "Uttarakhand"
]

