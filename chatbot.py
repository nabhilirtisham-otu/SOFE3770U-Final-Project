from dotenv import load_dotenv
load_dotenv()

from google import genai
import os

def get_gemini_response(user_input, soh_value=None):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "❌ API key not found. Check your .env file."

    client = genai.Client(api_key=api_key)

    context = ""
    if soh_value is not None:
        context = f"The predicted battery SOH is {soh_value:.2f}%. "

    prompt = context + (
        "You are a battery health expert. "
        "Suggest safe, practical ways to keep lithium batteries healthy. "
        "Answer clearly and simply. "
        f"User question: {user_input}"
    )

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text
