import streamlit as st
from PIL import Image

from services.gemini_service import analyze_plant_image
from translations import translations
st.set_page_config(
    page_title="Smart Pesticide Assistant",
    page_icon="🌱"
)
language = st.sidebar.selectbox(
    "Language",
    ["English", "Telugu", "Hindi"]
)
provider = st.sidebar.selectbox(
    "AI Provider",
    ["Gemini", "Ollama"]
)
if ai_provider == "Gemini":
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password"
    )
st.sidebar.info(
    "Supports English, Telugu and Hindi."
)

st.sidebar.info(
    "Bring your own Gemini API Key or use local AI."
)
st.title(
    translations[language]["title"]
)
st.success("AI-Powered Crop Disease Detection & Pesticide Recommendation System")
st.write(
    "Upload a crop leaf image to identify diseases and get pesticide recommendations."
)

uploaded_file = st.file_uploader(
    translations[language]["upload"],
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Crop Image",
        use_container_width=True
    )

    with st.spinner("Analyzing crop..."):

       result = analyze_plant_image(
    image,
    language,
    api_key
)

    st.subheader("Diagnosis Report")

    st.markdown(result)
    st.warning(
    translations[language]["warning"]
)