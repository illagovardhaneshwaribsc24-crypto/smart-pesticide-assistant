import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_plant_image(image, language, api_key=None):
    if api_key:
      genai.configure(api_key=api_key)
    prompt = f"""
You are an agricultural expert.

IMPORTANT LANGUAGE RULE:

The selected language is: {language}

If the selected language is Telugu:
- Write EVERYTHING in Telugu.
- Do NOT use English sentences.
- Translate all headings and explanations into Telugu.

If the selected language is Hindi:
- Write EVERYTHING in Hindi.
- Do NOT use English sentences.

If the selected language is English:
- Write EVERYTHING in English.

Analyze the crop image and provide:

Crop Name
Disease Name
Cause
Recommended Pesticide
Dosage
Organic Alternative
Prevention Tips

Return the complete response only in {language}.
"""
    response = model.generate_content(
        [prompt, image]
    )

    return response.text