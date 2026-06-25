import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import requests
import streamlit as st

from backend.services.recommendation_engine import get_recommendation
from backend.services.gemini_service import analyze_plant_image
from translations import translations


def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "qwen3:8b", "prompt": prompt, "stream": False},
            timeout=120,
        )

        data = response.json()
        return data.get("response", "")

    except requests.exceptions.Timeout:
        return "Ollama is taking too long. Please try again."

    except Exception as e:
        return f"Ollama Error: {e}"


st.set_page_config(
    page_title="Smart Pesticide Assistant",
    page_icon="🌱",
    layout="wide",  # Enhanced layout to support tabs gracefully
)

# Sidebar configurations
language = st.sidebar.selectbox("Language", ["English", "Telugu", "Hindi"])
provider = st.sidebar.selectbox("AI Provider", ["Gemini", "Ollama"])
st.sidebar.info("Supports English, Telugu and Hindi.")
st.sidebar.info("Bring your own Gemini API Key or use local AI.")

if provider == "Gemini":
    api_key = st.sidebar.text_input(
        "Gemini API Key", type="password", key="gemini_api_key"
    )
    if not api_key:
        st.sidebar.warning("Enter your Gemini API Key to continue.")
        # We don't use st.stop() here so they can browse other tabs without an API key immediately.
else:
    api_key = None

# Global headers
st.title(translations[language]["title"])
st.success(translations[language]["subtitle"])

# Creating App Tabs for Navigation
tab1, tab2, tab3, tab4 = st.tabs(translations[language]["tabs"])

# --- TAB 1: CROP DIAGNOSIS (With Explainable AI) ---
with tab1:
    st.write(translations[language]["description"])

    from backend.services.image_utils import load_image
    from backend.services.weather_advisor import get_weather_advice

    uploaded_file = st.file_uploader(
        translations[language]["upload"],
        type=["jpg", "jpeg", "png"],
        key="crop_uploader",
    )

    if uploaded_file:
        image = load_image(uploaded_file)
        st.image(image, caption="Uploaded Crop Image", use_container_width=True)

        if provider == "Gemini" and not api_key:
            st.error("Please enter your Gemini API Key in the sidebar to run analysis.")
        else:
            with st.spinner("Analyzing crop..."):
                result = analyze_plant_image(image, language, api_key)

            st.success("✅ Analysis Completed")
            st.divider()

            st.subheader("📋 Diagnosis Report")
            st.markdown(result)

            st.subheader("🌿 Pesticide Recommendation")

            disease = st.text_input("Enter detected disease (e.g., rust, blight)")

            if disease:
                recommendation = get_recommendation(disease)
                st.success(recommendation)

            st.info("💡 Explainable AI Insights:")
            st.caption("AI detected leaf discoloration, lesions, and texture anomalies.")

            st.warning(translations[language]["warning"])


# --- TAB 2: AI CHATBOT FOR FARMERS ---
# --- TAB 2: AI CHATBOT FOR FARMERS ---
with tab2:
    st.header(translations[language]["chatbot_header"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    prompt = st.chat_input(translations[language]["chatbot_placeholder"])

    if prompt:
        # User message
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        # Assistant reply
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if provider == "Ollama":
                    full_prompt = f"""
You are AgriBot, an expert agricultural assistant for Indian farmers.

Rules:
- Answer only agriculture, crops, pests, diseases, fertilizers, irrigation, weather and farming questions.

- If the question is NOT agriculture related:
  - Telugu: "నేను వ్యవసాయ సంబంధిత ప్రశ్నలకు మాత్రమే సమాధానం ఇస్తాను."
  - Hindi: "मैं केवल कृषि संबंधी प्रश्नों का उत्तर दे सकता हूँ।"
  - English: "I can only answer agriculture-related questions."

- If language is Telugu, answer in Telugu.
- If language is Hindi, answer in Hindi.
- If language is English, answer in English.
- If the question is written in Roman Telugu (English letters), understand it and reply in Telugu script.

Examples:

Question: Vari pantalo blast disease lakshanalu enti?
Answer:
వరి పంటలో బ్లాస్ట్ వ్యాధి ముఖ్య లక్షణాలు:
• ఆకులపై వజ్రాకారపు గోధుమ రంగు మచ్చలు కనిపిస్తాయి.
• ఆకులు ఎండిపోవచ్చు.
• దిగుబడి తగ్గే అవకాశం ఉంటుంది.

Question: Patti pantalo aphids ki mandu enti?
Answer:
పత్తి పంటలో ఆఫిడ్స్ నియంత్రణకు ఇమిడాక్లోప్రిడ్ లేదా థియామెథాక్సామ్ వంటి మందులను వ్యవసాయ అధికారుల సూచన మేరకు ఉపయోగించండి.

Question: Tomato mokkaki aakulu pasupu ga avutunnayi enduku?
Answer:
టమాటా ఆకులు పసుపు రంగులోకి మారడానికి పోషక లోపం, వైరస్ లేదా నీటి నిర్వహణ సమస్యలు కారణం కావచ్చు.

Now answer the farmer's question.

Language: {language}

Question:
{prompt}

Answer:
"""

                    reply = ask_ollama(full_prompt)

                else:
                    reply = (
                        f"Thank you for asking about '{prompt}'. "
                        "Please configure Gemini integration."
                    )

                st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

# --- TAB 3: WEATHER-BASED SPRAY RECOMMENDATION ---
with tab3:
    st.header(translations[language]["weather_header"])
    st.write(
        "Check if today's ambient conditions are safe for executing pesticide applications."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        temp = st.slider("Temperature (°C)", 15, 45, 28)
    with col2:
        wind = st.slider("Wind Speed (km/h)", 0, 30, 8)
    with col3:
        humidity = st.slider("Humidity (%)", 10, 100, 60)

    # Logic checklist evaluation
    st.subheader("Assessment Dashboard")
    if wind > 15:
        st.error(
            "❌ **Do Not Spray Now!** High winds will cause pesticide drift away from targeted targets."
        )
    elif temp > 38:
        st.warning(
            "⚠️ **Caution:** High ambient temperatures reduce spray efficacy due to accelerated evaporation risks."
        )
    elif humidity > 85:
        st.warning(
            "⚠️ **Caution:** Excessive moisture levels might clear chemical residues before absorption happens."
        )
    else:
        st.success(
            "✅ **Optimal Conditions:** Safe parameters verified! Good time to apply treatments."
        )
    if st.button("Get AI Weather Advice"):
       advice = get_weather_advice(temp, wind, humidity)
       st.info(advice)

# --- TAB 4: COST ESTIMATION ---
with tab4:
    st.header(translations[language]["cost_header"])

    col_a, col_b = st.columns(2)
    with col_a:
        farm_size = st.number_input(
            "Farm Size (Acres)", min_value=0.1, max_value=100.0, value=1.0, step=0.5
        )
        pesticide_price = st.number_input(
            "Pesticide Cost per Liter (💵)", min_value=100, max_value=5000, value=800
        )
    with col_b:
        dosage = st.number_input(
            "Dosage required per Acre (Liters)",
            min_value=0.1,
            max_value=10.0,
            value=1.5,
            step=0.1,
        )
        labor_cost = st.number_input(
            "Labor cost per Acre (💵)", min_value=0, max_value=2000, value=400
        )

    if st.button(translations[language]["estimate_btn"]):
        chemical_expense = farm_size * dosage * pesticide_price
        labor_expense = farm_size * labor_cost
        total_expense = chemical_expense + labor_expense

        st.divider()
        st.metric(
            label="Total Estimated Operational Budget Required",
            value=f"₹ {total_expense:,.2f}",
        )

        # Display cost data breakdown table
        cost_breakdown = {
            "Expense Type": [
                "Pesticide Formulation Costs",
                "Labor/Application Costs",
                "Total Gross Budget Request",
            ],
            "Calculated Share": [
                f"₹ {chemical_expense:,.2f}",
                f"₹ {labor_expense:,.2f}",
                f"₹ {total_expense:,.2f}",
            ],
        }
        st.table(cost_breakdown)
75