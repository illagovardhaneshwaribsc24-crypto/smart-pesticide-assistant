import sys
from pathlib import Path

# Add project root to path for backend imports
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from google import genai

# Backend service imports
from backend.services.recommendation_engine import get_recommendation
from backend.services.gemini_service import analyze_plant_image
from backend.services.weather_advisor import get_weather_advice
from backend.services.image_utils import load_image
from translations import translations

# Gemini API client initialization
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

def ask_gemini(prompt):
    """Helper function to get conversational text responses from Gemini."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gemini Error: {e}"

# Page configuration
st.set_page_config(
    page_title="Smart Pesticide Assistant",
    page_icon="🌱",
    layout="wide"
)

# ==========================
# SIDEBAR
# ==========================
language = st.sidebar.selectbox(
    "Language",
    ["English", "Telugu", "Hindi"]
)

st.sidebar.info("🌱 Powered by Gemini AI")
st.sidebar.info("Supports English, Telugu and Hindi")

# ==========================
# HEADER
# ==========================
st.title(translations[language]["title"])
st.success(translations[language]["subtitle"])

# Setup App Tabs
tab1, tab2, tab3, tab4 = st.tabs(translations[language]["tabs"])

# ==========================
# TAB 1: CROP DIAGNOSIS
# ==========================
with tab1:
    st.write(translations[language]["description"])

    uploaded_file = st.file_uploader(
        translations[language]["upload"],
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = load_image(uploaded_file)
        
        st.image(
            image,
            caption="Uploaded Crop Image",
            use_container_width=True
        )

        with st.spinner("Analyzing crop with Gemini..."):
            result = analyze_plant_image(image, language)

        st.success("✅ Analysis Completed")
        st.subheader("📋 Diagnosis Report")
        st.markdown(result)

        st.subheader("🌿 Pesticide Recommendation")
        disease = st.text_input("Enter detected disease")

        if disease:
            recommendation = get_recommendation(disease)
            st.success(recommendation)

        st.info("💡 Explainable AI Insights")
        st.caption("Gemini analyzed leaf symptoms, color changes and visible patterns.")

# ==========================
# TAB 2: CHATBOT (AgriBot)
# ==========================
with tab2:
    st.header(translations[language]["chatbot_header"])

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display historical messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User chat input
    prompt = st.chat_input(translations[language]["chatbot_placeholder"])

    if prompt:
        # 1. Append and display User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Structure context prompt for the model
        full_prompt = f"""
You are AgriBot, an agricultural expert.
Answer only farming related questions.

Language: {language}
Farmer question: {prompt}

Give a helpful farming answer.
"""

        # 3. Fetch response from Gemini and display
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = ask_gemini(full_prompt)
            st.markdown(reply)

        # 4. Append Assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ==========================
# TAB 3: WEATHER ADVISOR
# ==========================
with tab3:
    st.header(translations[language]["weather_header"])

    temp = st.slider("Temperature °C", 15, 45, 28)
    wind = st.slider("Wind Speed km/h", 0, 30, 8)
    humidity = st.slider("Humidity %", 10, 100, 60)

    # Static alert thresholds
    if wind > 15:
        st.error("❌ High wind. Avoid spraying.")
    elif temp > 38:
        st.warning("⚠️ Temperature too high.")
    elif humidity > 85:
        st.warning("⚠️ High humidity.")
    else:
        st.success("✅ Good spraying conditions.")

    if st.button("Get AI Weather Advice"):
        advice = get_weather_advice(temp, wind, humidity)
        st.info(advice)

# ==========================
# TAB 4: COST ESTIMATOR
# ==========================
with tab4:
    st.header(translations[language]["cost_header"])

    farm_size = st.number_input("Farm Size Acres", 0.1, 100.0, 1.0)
    pesticide_price = st.number_input("Pesticide price per liter", 100, 5000, 800)
    dosage = st.number_input("Dosage per acre", 0.1, 10.0, 1.5)
    labor_cost = st.number_input("Labor cost per acre", 0, 2000, 400)

    if st.button(translations[language]["estimate_btn"]):
        chemical_cost = farm_size * dosage * pesticide_price
        labor_total = farm_size * labor_cost
        total_budget = chemical_cost + labor_total

        st.metric(
            label="Total Budget",
            value=f"₹ {total_budget:,.2f}"
        )