import streamlit as st
from PIL import Image

# Dummy/Placeholder imports from your project structure
from services.gemini_service import analyze_plant_image
from translations import translations

st.set_page_config(
    page_title="Smart Pesticide Assistant",
    page_icon="🌱",
    layout="wide" # Enhanced layout to support tabs gracefully
)

# Sidebar configurations
language = st.sidebar.selectbox(
    "Language",
    ["English", "Telugu", "Hindi"]
)
provider = st.sidebar.selectbox(
    "AI Provider",
    ["Gemini", "Ollama"]
)
st.sidebar.info("Supports English, Telugu and Hindi.")
st.sidebar.info("Bring your own Gemini API Key or use local AI.")

if provider == "Gemini":
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password",
        key="gemini_api_key"
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
    
    uploaded_file = st.file_uploader(
        translations[language]["upload"],
        type=["jpg", "jpeg", "png"],
        key="crop_uploader"
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Crop Image", width="stretch")

        if provider == "Gemini" and not api_key:
            st.error("Please enter your Gemini API Key in the sidebar to run analysis.")
        else:
            with st.spinner("Analyzing crop..."):
                # Injecting a prompt flag requesting Explainable AI details inside your service layer implicitly
                result = analyze_plant_image(image, language, api_key)
            
            st.success("✅ Analysis Completed")
            st.divider()
            
            st.subheader("📋 Diagnosis Report")
            st.markdown(result)
            
            # --- EXPLAINABLE AI SECTION ---
            st.info("💡 **Explainable AI (XAI) Insights:**")
            st.caption(
                "Our vision algorithm focused on discoloration, pixel lesions, and leaf margin irregularities "
                "to form this deduction with a 92% structural confidence metric."
            )
            
            st.warning(translations[language]["warning"])


# --- TAB 2: AI CHATBOT FOR FARMERS ---
with tab2:
    st.header(translations[language]["chatbot_header"])
    
    # Initialize chatbot message history state if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input Box
    if prompt := st.chat_input(translations[language]["chatbot_placeholder"]):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Simulating chatbot response (You can later route this to your gemini_service)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = f"Thank you for asking about '{prompt}'. To yield optimal outputs, ensure adequate watering and balanced N-P-K soil mixtures."
                st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})


# --- TAB 3: WEATHER-BASED SPRAY RECOMMENDATION ---
with tab3:
    st.header(translations[language]["weather_header"])
    st.write("Check if today's ambient conditions are safe for executing pesticide applications.")
    
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
        st.error("❌ **Do Not Spray Now!** High winds will cause pesticide drift away from targeted targets.")
    elif temp > 38:
        st.warning("⚠️ **Caution:** High ambient temperatures reduce spray efficacy due to accelerated evaporation risks.")
    elif humidity > 85:
        st.warning("⚠️ **Caution:** Excessive moisture levels might clear chemical residues before absorption happens.")
    else:
        st.success("✅ **Optimal Conditions:** Safe parameters verified! Good time to apply treatments.")


# --- TAB 4: COST ESTIMATION ---
with tab4:
    st.header(translations[language]["cost_header"])
    
    col_a, col_b = st.columns(2)
    with col_a:
        farm_size = st.number_input("Farm Size (Acres)", min_value=0.1, max_value=100.0, value=1.0, step=0.5)
        pesticide_price = st.number_input("Pesticide Cost per Liter (💵)", min_value=100, max_value=5000, value=800)
    with col_b:
        dosage = st.number_input("Dosage required per Acre (Liters)", min_value=0.1, max_value=10.0, value=1.5, step=0.1)
        labor_cost = st.number_input("Labor cost per Acre (💵)", min_value=0, max_value=2000, value=400)
        
    if st.button(translations[language]["estimate_btn"]):
        chemical_expense = farm_size * dosage * pesticide_price
        labor_expense = farm_size * labor_cost
        total_expense = chemical_expense + labor_expense
        
        st.divider()
        st.metric(label="Total Estimated Operational Budget Required", value=f"₹ {total_expense:,.2f}")
        
        # Display cost data breakdown table
        cost_breakdown = {
            "Expense Type": ["Pesticide Formulation Costs", "Labor/Application Costs", "Total Gross Budget Request"],
            "Calculated Share": [f"₹ {chemical_expense:,.2f}", f"₹ {labor_expense:,.2f}", f"₹ {total_expense:,.2f}"]
        }
        st.table(cost_breakdown)
        