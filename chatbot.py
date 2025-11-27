import re
import os
from dotenv import load_dotenv
from google import genai

#Load API key from .env
load_dotenv()

def get_gemini_response(user_input, soh_value=None):

    #Get the API key
    api_key = os.getenv("GEMINI_API_KEY")

    #Error handler for missing API key
    if not api_key:
        return "API key not found. Please check your .env file."

    #Create Gemini client
    client = genai.Client(api_key=api_key)

    #Build context using SOH value
    context = ""
    if soh_value is not None:
        context = f"The predicted battery State of Health (SOH) is {soh_value:.2f}. "

    #Battery topic guard list
    battery_keywords = [
    "battery", "soh", "soc", "charge", "charging", "voltage", "cell",
    "degradation", "capacity", "lithium", "cycle", "power", "drain",
    "overheat", "storage", "temperature", "health", "pack", "batteries",
    "state of health", "health index", "remaining useful life", "rul",
    "aging", "wear", "capacity loss", "capacity fade",
    "calendar aging", "cycle aging", "lifespan", "lifetime",
    "state of charge", "depth of discharge", "dod",
    "cycle count", "full equivalent cycles", "fec",
    "discharge", "discharging", "overcharge", "overcharging",
    "overdischarge", "fast charge", "trickle charge",
    "internal resistance", "impedance", "voltage sag", "voltage drop",
    "efficiency", "energy density", "power density",
    "battery health", "health monitoring", "health estimation",
    "diagnostics", "fault detection", "condition monitoring",
    "predictive maintenance", "trend analysis", "telemetry",
    "data logging", "health reporting",
    "capacity test", "load test", "impedance test", "pulse test",
    "open circuit voltage", "ocv", "cycle testing",
    "thermal stress", "overheating", "heat exposure",
    "cold performance", "high c-rate", "fast charging",
    "thermal runaway", "swelling", "leakage", "internal short",
    "dendrite", "gas generation", "electrolyte breakdown",
    "end of life", "eol", "second life", "reconditioning",
    "repurposing", "recycling"
]

    

    #Block unrelated questions
    if not any(word in user_input.lower() for word in battery_keywords):
        return "I can only answer battery-related questions. Please ask about battery health, charging, SOH, lifespan, or safety."

    #AI instruction + prompt
    prompt = context + (
        "You are a professional battery health assistant for a university research project. "
        "You only answer questions related to batteries, battery health, charging, safety, maintenance, lifecycle, and SOH. "
        "Respond clearly and professionally.\n\n"
        f"User Question: {user_input}"
    )

    #Generate response and define model
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text
