# backend/services/gemini_service.py
import streamlit as st
from google import genai

def analyze_plant_image(image, language):
    """
    Analyzes the plant image using the new google-genai SDK.
    'image' should be a PIL Image object loaded by your load_image utility.
    """
    try:
        # Re-initialize or pass the client. 
        # Best practice is to fetch it from st.secrets if not passed as an argument.
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        
        prompt = f"""
        You are an expert plant pathologist. Analyze this crop image and provide a detailed diagnosis report.
        Identify any visible diseases, nutrient deficiencies, or pest infestations.
        
        Provide the response completely in the following language: {language}
        """
        
        # With the new SDK, you can pass the PIL Image object directly in the contents list
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[image, prompt]  # Pass both the PIL Image and the text prompt here
        )
        
        return response.text

    except Exception as e:
        return f"Gemini Error inside service layer: {e}"