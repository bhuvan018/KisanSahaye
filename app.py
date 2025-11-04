import streamlit as st
from PIL import Image
import io
from utils.gemini_service import (
    analyze_crop_disease,
    analyze_soil_quality,
    get_crop_recommendations,
    chat_with_ai
)
from utils.weather_service import (
    get_weather_data,
    get_weather_recommendations,
    format_weather_info
)
from utils.market_service import get_market_insights, get_all_crop_prices
from config import ALL_CROPS, INDIAN_STATES

# Page configuration
st.set_page_config(
    page_title="Krishi Mitra - AI Agriculture Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2e7d32;
        padding: 20px;
    }
    /* Primary buttons styling - only if they don't have kind="secondary" */
    .stButton>button:not([kind="secondary"]) {
        min-height: 32px !important;
        height: 32px !important;
        padding: 6px 20px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton>button:not([kind="secondary"]):hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    /* Base styling for all feature cards */
    div[data-testid="stButton"] > button[kind="secondary"] {
        width: 100%;
        min-height: 5px;
        border-radius: 16px !important;
        padding: 18px 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        white-space: pre-line !important;
        text-align: center !important;
        line-height: 1.6 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    /* Add JavaScript to inject data attributes for easier targeting */
    </style>
    <script>
    setTimeout(function() {
        const buttons = document.querySelectorAll('div[data-testid="stButton"] > button[kind="secondary"]');
        buttons.forEach((btn, idx) => {
            if (btn.textContent.includes('Disease Detection')) {
                btn.classList.add('feature-disease');
            } else if (btn.textContent.includes('Weather Recommendations')) {
                btn.classList.add('feature-weather');
            } else if (btn.textContent.includes('Soil Analysis')) {
                btn.classList.add('feature-soil');
            } else if (btn.textContent.includes('Market Prices')) {
                btn.classList.add('feature-market');
            } else if (btn.textContent.includes('Crop Diversification')) {
                btn.classList.add('feature-diversification');
            } else if (btn.textContent.includes('Ask Expert')) {
                btn.classList.add('feature-expert');
            }
        });
    }, 100);
    </script>
    <style>
    /* Disease Detection - Red/Orange theme */
    button.feature-disease {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%) !important;
        border: 2px solid #ff6b6b !important;
        color: #c92a2a !important;
    }
    button.feature-disease:hover {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%) !important;
        border-color: #ef5350 !important;
        box-shadow: 0 8px 16px rgba(255, 107, 107, 0.3) !important;
        transform: translateY(-4px) scale(1.02) !important;
    }
    
    /* Weather Recommendations - Blue/Sky theme */
    button.feature-weather {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%) !important;
        border: 2px solid #42a5f5 !important;
        color: #1565c0 !important;
    }
    button.feature-weather:hover {
        background: linear-gradient(135deg, #bbdefb 0%, #90caf9 100%) !important;
        border-color: #1e88e5 !important;
        box-shadow: 0 8px 16px rgba(66, 165, 245, 0.3) !important;
        transform: translateY(-4px) scale(1.02) !important;
    }
    
    /* Soil Analysis - Brown/Earth theme */
    button.feature-soil {
        background: linear-gradient(135deg, #efebe9 0%, #d7ccc8 100%) !important;
        border: 2px solid #8d6e63 !important;
        color: #5d4037 !important;
    }
    button.feature-soil:hover {
        background: linear-gradient(135deg, #d7ccc8 0%, #bcaaa4 100%) !important;
        border-color: #6d4c41 !important;
        box-shadow: 0 8px 16px rgba(141, 110, 99, 0.3) !important;
        transform: translateY(-4px) scale(1.02) !important;
    }
    
    /* Market Prices - Gold/Yellow theme */
    button.feature-market {
        background: linear-gradient(135deg, #fffde7 0%, #fff9c4 100%) !important;
        border: 2px solid #fbc02d !important;
        color: #f57f17 !important;
    }
    button.feature-market:hover {
        background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%) !important;
        border-color: #f9a825 !important;
        box-shadow: 0 8px 16px rgba(251, 192, 45, 0.3) !important;
        transform: translateY(-4px) scale(1.02) !important;
    }
    
    /* Crop Diversification - Purple/Green theme */
    button.feature-diversification {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%) !important;
        border: 2px solid #ab47bc !important;
        color: #7b1fa2 !important;
    }
    button.feature-diversification:hover {
        background: linear-gradient(135deg, #e1bee7 0%, #ce93d8 100%) !important;
        border-color: #8e24aa !important;
        box-shadow: 0 8px 16px rgba(171, 71, 188, 0.3) !important;
        transform: translateY(-4px) scale(1.02) !important;
    }
    
    /* Ask Expert - Teal/Cyan theme */
    button.feature-expert {
        background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%) !important;
        border: 2px solid #26c6da !important;
        color: #00838f !important;
    }
    button.feature-expert:hover {
        background: linear-gradient(135deg, #b2ebf2 0%, #80deea 100%) !important;
        border-color: #00acc1 !important;
        box-shadow: 0 8px 16px rgba(38, 198, 218, 0.3) !important;
        transform: translateY(-4px) scale(1.02) !important;
    }
    
    /* Style the first line (icon) to be larger */
    div[data-testid="stButton"] > button[kind="secondary"]:first-line {
        font-size: 40px !important;
        line-height: 1.2 !important;
        display: block !important;
        margin-bottom: 8px !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🌾 Krishi Mitra - AI Agriculture Assistant</h1>', unsafe_allow_html=True)
st.markdown("### Empowering Indian Farmers with AI-Powered Agricultural Solutions")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "🏠 Home"

# Sidebar navigation
st.sidebar.title("🌾 Navigation")
page_options = ["🏠 Home", "🔍 Disease Detection", "🌦️ Weather Recommendations", "🌱 Soil Analysis", 
                "🔄 Crop Diversification", "💬 Ask Expert"]

try:
    default_index = page_options.index(st.session_state.selected_page)
except ValueError:
    default_index = 0

page = st.sidebar.radio(
    "Choose a feature:",
    page_options,
    index=default_index
)

# Update session state if page changed from sidebar
if page != st.session_state.selected_page:
    st.session_state.selected_page = page

# Home Page
if page == "🏠 Home":
    st.header("Welcome to Krishi Mitra!")
    st.markdown("""
    **Your AI-powered agricultural assistant designed specifically for Indian farmers.**
    """)
    
    st.markdown("### Available Features:")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Define features with icons, titles, and descriptions
    features = [
        {
            "icon": "🔍",
            "title": "Disease Detection",
            "page": "🔍 Disease Detection",
            "description": "Identify crop diseases and pests"
        },
        {
            "icon": "🌦️",
            "title": "Weather Recommendations",
            "page": "🌦️ Weather Recommendations",
            "description": "Get weather-based advice"
        },
        {
            "icon": "🌱",
            "title": "Soil Analysis",
            "page": "🌱 Soil Analysis",
            "description": "Analyze soil quality"
        },
        {
            "icon": "🔄",
            "title": "Crop Diversification",
            "page": "🔄 Crop Diversification",
            "description": "Get crop suggestions"
        },
        {
            "icon": "💬",
            "title": "Ask Expert",
            "page": "💬 Ask Expert",
            "description": "Chat with AI expert"
        }
    ]
    
    # Create grid layout: 3 columns, 2 rows
    cols = st.columns(3)
    
    for idx, feature in enumerate(features):
        col_idx = idx % 3
        
        with cols[col_idx]:
            # Create button styled as a feature card
            # Format: Icon (large), Title, Description
            button_text = f"{feature['icon']}\n\n{feature['title']}\n\n{feature['description']}"
            if st.button(
                button_text,
                key=f"feature_btn_{idx}",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state.selected_page = feature['page']
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 Click on any feature card above or use the sidebar to get started! 🚀")

# Disease Detection Page
elif page == "🔍 Disease Detection":
    st.header("🔍 Crop Disease & Pest Detection")
    st.markdown("Upload an image of your crop to identify diseases, pests, and get treatment recommendations.")
    
    crop_name = st.selectbox("Select Crop Type (Optional)", [""] + ALL_CROPS)
    
    uploaded_file = st.file_uploader(
        "Upload Crop Image",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of the affected crop part"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=500)
        
        if st.button("🔍 Analyze Disease"):
            with st.spinner("Analyzing image with AI..."):
                result = analyze_crop_disease(image, crop_name)
                st.success("Analysis Complete!")
                st.markdown("### Analysis Results:")
                st.info(result)

# Weather Recommendations Page
elif page == "🌦️ Weather Recommendations":
    st.header("🌦️ Weather-Based Recommendations")
    st.markdown("Get weather-specific planting and care recommendations for your crops.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        city = st.text_input("City Name", placeholder="e.g., Mumbai")
        state = st.selectbox("State", [""] + INDIAN_STATES)
    
    with col2:
        crop_name = st.selectbox("Select Crop", [""] + ALL_CROPS)
    
    if st.button("Get Weather Recommendations"):
        if not city:
            st.error("Please enter a city name")
        else:
            with st.spinner("Fetching weather data..."):
                weather_data, error = get_weather_data(city, state)
                
                if error:
                    st.error(f"Error: {error}")
                elif weather_data:
                    st.success("Weather data retrieved!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### Current Weather")
                        st.markdown(format_weather_info(weather_data))
                    
                    with col2:
                        if crop_name:
                            st.markdown("### Crop-Specific Recommendations")
                            recommendations = get_weather_recommendations(crop_name, weather_data)
                            st.info(recommendations)
                        else:
                            st.info("Select a crop to get specific recommendations")

# Soil Analysis Page
elif page == "🌱 Soil Analysis":
    st.header("🌱 Soil Quality Analysis")
    st.markdown("Analyze soil quality from image or text description.")
    
    analysis_type = st.radio("Analysis Method", ["Image Upload", "Text Description"])
    
    if analysis_type == "Image Upload":
        uploaded_file = st.file_uploader(
            "Upload Soil Image",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of your soil"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Soil Image", width=500)
            
            if st.button("Analyze Soil"):
                with st.spinner("Analyzing soil quality..."):
                    result = analyze_soil_quality(image=image)
                    st.success("Analysis Complete!")
                    st.markdown("### Soil Analysis Results:")
                    st.info(result)
    
    else:
        description = st.text_area(
            "Describe your soil",
            placeholder="e.g., Red soil, sandy texture, low organic matter, pH around 6.5...",
            height=100
        )
        
        if st.button("Analyze Soil"):
            if description:
                with st.spinner("Analyzing soil description..."):
                    result = analyze_soil_quality(description=description)
                    st.success("Analysis Complete!")
                    st.markdown("### Soil Analysis Results:")
                    st.info(result)
            else:
                st.error("Please enter a soil description")


# Crop Diversification Page
elif page == "🔄 Crop Diversification":
    st.header("🔄 Crop Diversification Recommendations")
    st.markdown("Get AI-powered suggestions for diversifying your crops based on your region and soil.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        state = st.selectbox("State", [""] + INDIAN_STATES)
        district = st.text_input("District/City", placeholder="e.g., Nashik")
    
    with col2:
        soil_type = st.selectbox(
            "Soil Type",
            ["", "Loamy", "Clayey", "Sandy", "Red Soil", "Black Soil", "Alluvial", "Other"]
        )
        preferences = st.text_input("Preferences (Optional)", placeholder="e.g., prefer vegetables, low water requirement")
    
    if st.button("Get Recommendations"):
        if not state or not soil_type:
            st.error("Please fill in State and Soil Type")
        else:
            region = f"{district}, {state}" if district else state
            with st.spinner("Generating crop diversification recommendations..."):
                recommendations = get_crop_recommendations(region, soil_type, preferences)
                st.success("Recommendations Ready!")
                st.markdown("### Diversification Recommendations:")
                st.info(recommendations)

# Ask Expert Page
elif page == "💬 Ask Expert":
    st.header("💬 Ask Agricultural Expert")
    st.markdown("Chat with our AI expert for any agricultural questions.")
    
    # Display chat history
    for i, (role, message) in enumerate(st.session_state.chat_history):
        if role == "user":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**Krishi Mitra:** {message}")
        st.markdown("---")
    
    # User input
    question = st.text_input("Ask your question:", placeholder="e.g., How to prevent aphids on tomato plants?")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Send"):
            if question:
                with st.spinner("Thinking..."):
                    response = chat_with_ai(question)
                    st.session_state.chat_history.append(("user", question))
                    st.session_state.chat_history.append(("assistant", response))
                    st.rerun()
            else:
                st.error("Please enter a question")
    
    with col2:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()



