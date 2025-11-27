import re
import os
import json
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()


# ---------------- LOAD MODEL RESULTS ----------------
def load_battery_report():
    try:
        with open("battery_report.json", "r") as f:
            return json.load(f)
    except:
        return None


# ---------------- CHATBOT FUNCTION ----------------
def get_gemini_response(user_input, battery_report):

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "ERROR: GEMINI_API_KEY not found in .env file."

    client = genai.Client(api_key=api_key)

    battery_keywords = [
        "battery", "soh", "soc", "charge", "charging", "voltage", "cell",
        "degradation", "capacity", "lithium", "cycle", "power", "drain",
        "overheat", "storage", "temperature", "health", "pack", "batteries",
        "state of health", "rul", "lifespan", "aging", "capacity fade",
        "fast charge", "overcharging", "overdischarge", "internal resistance",
        "impedance", "thermal runaway", "swelling", "fault",
        "diagnostics", "maintenance", "prediction", "health monitoring"
    ]

    if not any(word in user_input.lower() for word in battery_keywords):
        return "I only answer battery-related questions."

    report = load_battery_report()

    context = ""

    if report:
        m = report["metrics"]
        cells = report["cells"]
        importance = report["feature_importance"]

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

        for i, c in enumerate(cells):
            context += f"Cell {i+1}: True={c['true soh']:.3f}, Pred={c['predicted soh']:.3f}, Status={c['status']}\n"

        context += "\nMOST IMPORTANT VOLTAGE FEATURES:\n"
        for k in list(importance.keys())[:5]:
            context += f"{k}: {importance[k]:.4f}\n"

    prompt = context + (
        "\nYou are a battery diagnostics assistant using real model data above. "
        "Explain performance, failures, safety, risks and recommendations clearly.\n\n"
        f"User Question: {user_input}"
    )

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text
