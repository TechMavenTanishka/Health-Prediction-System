# Generate AI-powered health remarks using Gemini
from prediction import predict_health_risk
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Create Gemini client
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key
)

# Generates professional medical remarks using Gemini AI

def generate_ai_remark(risk_prediction):

    prompt = f"""
    A patient has the following health risks:

    {risk_prediction}

    Generate a short professional medical remark
    in 2-3 sentences.

    Do not provide a final diagnosis.
    Recommend consulting a healthcare professional.
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"AI service temporarily unavailable: {str(e)}"


