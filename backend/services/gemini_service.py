import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
print("API KEY:", os.getenv("GEMINI_API_KEY"))

def analyze_plant_image(image, language, api_key=None):
    # Configure API key
    if api_key:
        print("USING SIDEBAR API KEY")
        genai.configure(api_key=api_key)
        key = api_key if api_key else os.getenv("GEMINI_API_KEY")
        print("Loaded key:", key[:10] if key else "None")
        genai.configure(api_key=key)
    else:
        print("USING .ENV API KEY")
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Initialize model
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Construct prompt
    prompt = f"""
    You are an agricultural expert.

    IMPORTANT LANGUAGE RULE:
    The selected language is: {language}

    Write the response in proper Markdown format.

    Use:

    ## 🌱 Crop Name

    ## 🦠 Disease Name

    ## ⚠️ Cause

    ## 💊 Recommended Pesticide

    ## 📏 Dosage

    ## 🌿 Organic Alternative

    ## ✅ Prevention Tips

    For Prevention Tips use bullet points.

    Leave one blank line between sections.

    Return the complete response only in {language}.
    """

    # Generate content
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"
