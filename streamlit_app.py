import streamlit as st
import subprocess
import os
import sys
from chatbot import get_gemini_response

# ---------------- CONFIG ----------------

st.set_page_config(page_title="Battery Health AI", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "LinearRegressionModel.py")
PYTHON_PATH = sys.executable
SOH_FILE = os.path.join(BASE_DIR, "latest_soh.txt")
PLOT_FILE = os.path.join(BASE_DIR, "soh_plot.png")

# ---------------- TITLE ----------------

st.title("🔋 Battery Health Assistant")
st.caption("SOH Prediction + Gemini AI Advisor")

# ---------------- CHAT ----------------

st.header("💬 Battery Advisor")

user_msg = st.text_input("Ask about battery health, charging, lifespan, or safety:")

soh_value = None

if os.path.exists(SOH_FILE):
    try:
        with open(SOH_FILE, "r") as f:
            soh_value = float(f.read().strip())
        st.metric("Predicted Battery SOH", f"{soh_value:.4f}")
    except Exception as e:
        st.error(f"Error reading SOH file: {e}")

if st.button("Ask AI"):
    if user_msg.strip() == "":
        st.warning("Please enter a question.")
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

    with st.spinner("Running regression model..."):

        result = subprocess.run(
            [PYTHON_PATH, MODEL_PATH],
            cwd=BASE_DIR,
            env=env,
            capture_output=True,
            text=True,
            shell=False
        )

    # ---------- OUTPUT ----------

    st.subheader("Model Output (STDOUT)")
    st.code(result.stdout)

    if result.stderr:
        st.subheader("Model Errors (STDERR)")
        st.code(result.stderr)

    # ---------- LOAD PLOT ----------

    if os.path.exists(PLOT_FILE):
        st.image(PLOT_FILE, caption="Predicted vs True SOH", use_container_width=True)
    else:
        st.warning("Plot file not found. Model may have failed.")

    # ---------- LOAD SOH ----------

    if os.path.exists(SOH_FILE):
        try:
            with open(SOH_FILE, "r") as f:
                soh_value = float(f.read().strip())
            st.success(f"SOH loaded successfully: {soh_value:.4f}")
        except:
            st.error("SOH file exists but could not be read.")
    else:
        st.warning("SOH file not generated.")

# ---------------- FOOTER ----------------

st.markdown("---")
st.caption("SOFE3770U Final Project | Battery Health AI")
