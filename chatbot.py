#import api key from env file
from dotenv import load_dotenv
load_dotenv()

#import the gemini chatbot
from google import genai
import os

def get_gemini_response(user_input, soh_value=None):

    #get the api key from the env file
    api_key = os.getenv("GEMINI_API_KEY")

    #error handler for api key
    if not api_key:
        return "API key not found. Check your .env file."

    #give the api key to the chatbot client and make a connection
    client = genai.Client(api_key=api_key)

    #give the chatbot context as what is happening with the battery and dataset
    context = ""
    if soh_value is not None:
        context = f"The predicted battery SOH is {soh_value:.2f}%. "

    #tell the chatbot the setting and how to act when asked questions
    prompt = context + (
    "You are a professional battery health assistant for a research project. "
    "You must ONLY answer questions related to batteries, battery health, charging, safety, maintenance, and SOH. "
    "If the user's question is NOT related to batteries, you must politely say you cannot answer it and redirect them to battery questions. "
    "Do not answer off-topic questions. "
    "Be Polite, respectful, and professional.\n\n"
    f"User question: {user_input}"
)


    #define what model of gemini we are using and generates response
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text
