import re
import os
import json
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()


#open json file and load data into chatbot
def load_battery_report():
    try:
        with open("battery_report.json", "r") as f:
            return json.load(f)
    except:
        return None



def get_gemini_response(user_input, battery_report):

    #define API key from .env file
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "ERROR: GEMINI_API_KEY not found in .env file."

    #make connection to the client with API key
    client = genai.Client(api_key=api_key)

    #Keywords that chatbot will respond to. If word is not in the user input chatbot will ignore
    battery_keywords = [
        "battery", "soh", "soc", "charge", "charging", "voltage", "cell",
        "degradation", "capacity", "lithium", "cycle", "power", "drain",
        "overheat", "storage", "temperature", "health", "pack", "batteries",
        "state of health", "rul", "lifespan", "aging", "capacity fade",
        "fast charge", "overcharging", "overdischarge", "internal resistance",
        "impedance", "thermal runaway", "swelling", "fault",
        "diagnostics", "maintenance", "prediction", "health monitoring"
    ]

    #ignore user input if no words are in defined words above
    if not any(word in user_input.lower() for word in battery_keywords):
        return "I only answer battery-related questions."

    report = load_battery_report()

    #initialize context variable for chatbot
    context = ""

    if report:
        m = report["metrics"]
        cells = report["cells"]
        importance = report["feature_importance"]

        #load context from report file into the context variable. Which will be passed to chatbot
        context += f""" 
MODEL PERFORMANCE:
R²: {m["r2"]:.4f}
MSE: {m["mse"]:.4f}
MAE: {m["mae"]:.4f}

SOH SUMMARY:
Average SOH: {m["avg_soh"]:.2f}
Threshold: {m["threshold"]}
PASS: {m["pass_count"]}   FAIL: {m["fail_count"]}

CELL STATUS:
"""
        #loads per cell information into the chatbot
        for i, c in enumerate(cells):
            context += f"Cell {i+1}: True={c['true soh']:.3f}, Pred={c['predicted soh']:.3f}, Status={c['status']}\n"

        #tells the chatbot which cells impact the SOH of the battery the most
        context += "\nMOST IMPORTANT VOLTAGE FEATURES:\n"
        for k in list(importance.keys())[:5]:
            context += f"{k}: {importance[k]:.4f}\n"

    #define how the AI chatbot should respond to user inputs
    prompt = context + (
        "\nYou are a battery diagnostics assistant using real model data above. "
        "Explain performance, failures, safety, risks and recommendations clearly.\n\n"
        f"User Question: {user_input}"
    )

    #define what model of Gemini is going to usd
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text
