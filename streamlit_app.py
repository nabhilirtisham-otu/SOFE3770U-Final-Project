import streamlit as st
import subprocess
import os
import sys
from chatbot import get_gemini_response

st.set_page_config(page_title="Battery Health AI", layout="centered")

BASE_DIR = os.path.dirname(__file__)

st.title("🔋 Battery Health Assistant")
st.caption("SOH Prediction + Gemini AI Advisor")

# ---------------- CHAT ----------------

st.header("💬 Battery Advisor")

user_msg = st.text_input("Ask about battery health, charging, lifespan, or safety:")

soh_file = os.path.join(BASE_DIR, "latest_soh.txt")
soh_value = None

if os.path.exists(soh_file):
    try:
        with open(soh_file) as f:
            soh_value = float(f.read().strip())
        st.metric("Predicted Battery SOH", f"{soh_value:.4f}")
    except:
        st.error("Error reading SOH file")

if st.button("Ask AI"):
    if user_msg.strip() == "":
        st.warning("Enter a question.")
    elif soh_value is None:
        st.error("Run the model first to generate SOH.")
    else:
        reply = get_gemini_response(user_msg, soh_value)
        st.success("AI Response")
        st.write(reply)

# ---------------- MODEL ----------------

st.header("📊 Linear Regression Model")

threshold = st.number_input(
    "SOH Fail Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.6,
    step=0.05
)

if st.button("Run SOH Prediction Model"):
    env = os.environ.copy()
    env["SOH_THRESHOLD"] = str(threshold)

    with st.spinner("Running model..."):
        result = subprocess.run(
            [os.sys.executable, "LinearRegressionModel.py"],
            cwd=BASE_DIR,
            env=env,
            capture_output=True,
            text=True
        )

    st.text_area("Model Output", result.stdout, height=300)

    if result.stderr:
        st.error("Errors:")
        st.text(result.stderr)

    plot_path = os.path.join(BASE_DIR, "soh_plot.png")

    if os.path.exists(plot_path):
        st.image(plot_path, caption="Predicted vs True SOH", use_column_width=True)
    else:
        st.warning("Plot file not found.")

# ---------------- FOOTER ----------------

st.markdown("---")
st.caption("SOFE3770U Final Project | Battery Health AI")
