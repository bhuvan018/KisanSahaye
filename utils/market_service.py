from datetime import datetime
import random

# Mock market data - In production, this would connect to real agricultural price APIs
# Free options: eNAM (Indian government), or web scraping from agri websites

MARKET_DATA = {
    "Rice": {"price": 2800, "unit": "₹/quintal", "trend": "stable"},
    "Wheat": {"price": 2400, "unit": "₹/quintal", "trend": "rising"},
    "Tomato": {"price": 35, "unit": "₹/kg", "trend": "volatile"},
    "Onion": {"price": 25, "unit": "₹/kg", "trend": "stable"},
    "Potato": {"price": 18, "unit": "₹/kg", "trend": "falling"},
    "Cotton": {"price": 7500, "unit": "₹/quintal", "trend": "rising"},
    "Sugarcane": {"price": 310, "unit": "₹/quintal", "trend": "stable"},
    "Chickpea": {"price": 5200, "unit": "₹/quintal", "trend": "rising"},
    "Groundnut": {"price": 6800, "unit": "₹/quintal", "trend": "stable"},
    "Mustard": {"price": 5500, "unit": "₹/quintal", "trend": "rising"},
    "Soybean": {"price": 4200, "unit": "₹/quintal", "trend": "falling"},
    "Turmeric": {"price": 150, "unit": "₹/kg", "trend": "rising"},
    "Chili": {"price": 180, "unit": "₹/kg", "trend": "volatile"},
    "Mango": {"price": 45, "unit": "₹/kg", "trend": "seasonal"},
    "Banana": {"price": 25, "unit": "₹/kg", "trend": "stable"},
}

def get_market_price(crop_name):
    """Get current market price for a crop"""
    crop_lower = crop_name.lower()
    
    # Try exact match first
    for crop, data in MARKET_DATA.items():
        if crop.lower() == crop_lower:
            return data
    
    # Try partial match
    for crop, data in MARKET_DATA.items():
        if crop_lower in crop.lower() or crop.lower() in crop_lower:
            return data
    
    # Default response
    return {
        "price": "N/A",
        "unit": "₹/quintal",
        "trend": "unknown",
        "note": "Price data not available. Check local mandi or eNAM website."
    }

def get_price_trend(crop_name):
    """Get price trend analysis"""
    data = get_market_price(crop_name)
    
    if isinstance(data, dict) and "trend" in data:
        trend = data["trend"]
        
        trend_explanations = {
            "rising": "📈 Prices are rising. Good time to plan harvesting and selling.",
            "falling": "📉 Prices are falling. Consider waiting if storage is possible.",
            "stable": "➡️ Prices are stable. Normal market conditions.",
            "volatile": "📊 Prices are volatile. Monitor closely before selling.",
            "seasonal": "🍃 Seasonal variation. Prices depend on harvest time."
        }
        
        return trend_explanations.get(trend, "Price trend data not available")
    
    return "Price trend data not available for this crop."

def get_market_insights(crop_name):
    """Get comprehensive market insights"""
    data = get_market_price(crop_name)
    
    if not isinstance(data, dict) or "price" not in data:
        return "Market data not available. Please check local mandi or agricultural market websites."
    
    insights = f"""
    **Current Market Price for {crop_name}:**
    - Price: {data.get('price', 'N/A')} {data.get('unit', '')}
    - Trend: {data.get('trend', 'unknown').title()}
    
    **Recommendations:**
    {get_price_trend(crop_name)}
    
    **Tips:**
    - Monitor prices regularly at your local mandi or eNAM portal
    - Consider selling when prices are favorable
    - Explore direct farmer-consumer markets for better margins
    - Check government MSP (Minimum Support Price) for applicable crops
    
    **Note:** This is sample data. For accurate prices, visit:
    - eNAM: https://www.enam.gov.in
    - Local agricultural mandi
    - State agricultural department websites
    """
    
    return insights

def get_all_crop_prices():
    """Get prices for all available crops"""
    return MARKET_DATA

