import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()


def analyze_plant_image(image, language, api_key=None):

    if api_key:
        print("USING SIDEBAR API KEY")
        genai.configure(api_key=api_key)
    else:
        print("USING .ENV API KEY")
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-2.5-flash")

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

    try:
        response = model.generate_content([prompt, image])

        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"
