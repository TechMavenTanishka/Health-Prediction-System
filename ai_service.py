# Generate AI-powered health remarks using Gemini
from prediction import predict_health_risk
import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

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
        # This catch-all intercepts both APIError and generic exceptions smoothly
        err_msg = str(e)
        
        # If the API hits a quota/rate limit block (429)
        if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
            # We return your excellent custom clinical summary text directly!
            return (
                f"Clinical Analysis Note: High cloud request volume detected. Based on your local screening results highlighting ({risk_prediction or 'General Assessment'}), "
                "the patient displays indicators that warrant further diagnostic monitoring. It is recommended to correlate these findings with a full metabolic panel "
                "and consult a primary care physician to establish a definitive preventative wellness strategy."
            )
            
        # If the API is completely down (503)
        elif "503" in err_msg or "UNAVAILABLE" in err_msg:
            return "ℹ️ Clinical Summary Notice: The Gemini AI consultation service is temporarily unavailable. Local diagnostic risk baselines remain fully active."
        
        # Generic fallback
        return "AI medical analysis engine is currently handling high volume traffic. Please cross-reference with local diagnostic risk thresholds."