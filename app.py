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
st.sidebar.info(
    "Supports English, Telugu and Hindi."
)

st.sidebar.info(
    "Bring your own Gemini API Key or use local AI."
)
st.title(
    translations[language]["title"]
)
st.success(
    translations[language]["subtitle"]
)

st.write(
    translations[language]["description"]
)

if provider == "Gemini":
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password",
        key="gemini_api_key"
    )

    if not api_key:
        st.warning("Enter your Gemini API Key to continue.")
        st.stop()
else:
    api_key = None

uploaded_file = st.file_uploader(
    translations[language]["upload"],
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Crop Image",
        width="stretch"
    )

    with st.spinner("Analyzing crop..."):

        result = analyze_plant_image(
            image,
            language,
            api_key
        )

    st.success("✅ Analysis Completed")

    st.divider()

    st.subheader("📋 Diagnosis Report")
    st.markdown(result)

    st.warning(
        translations[language]["warning"]
    )