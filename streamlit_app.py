import streamlit as st
import subprocess
import os
import sys
import json
from chatbot import get_gemini_response

#streamlit page styling
st.set_page_config(page_title="Battery Health AI", layout="centered")

#define files to used in the rest of the code 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "LinearRegressionModel.py")
PYTHON_PATH = sys.executable
REPORT_FILE = os.path.join(BASE_DIR, "battery_report.json")
PLOT_FILE = os.path.join(BASE_DIR, "soh_plot.png")

#streamlit page styling
st.title("Battery Health Assistant")
st.header("Battery Advisor")

#creates user input box
user_msg = st.text_input("Ask about battery health, charging, lifespan, or safety:")

#initialize report
report = None

st.header("Predicted SOH based on file:")

#load results file if it exists
if os.path.exists(REPORT_FILE):
    try:
        with open(REPORT_FILE, "r") as f:
            report = json.load(f)

        avg_soh = report["metrics"]["avg_soh"]
        r2 = report["metrics"]["r2"]
        mse = report["metrics"]["mse"]
        mae = report["metrics"]["mae"]

        st.metric("Predicted Battery SOH", f"{avg_soh:.4f}")
        st.caption(f"R²: {r2:.4f} | MSE: {mse:.4f} | MAE: {mae:.4f}")

    except Exception as e:
        st.error(f"Error reading report file: {e}")

#handle user inputs
if st.button("Ask AI"):
    if user_msg.strip() == "":
        st.warning("Please enter a question.")
    elif report is None:
        st.error("Run the model first to generate SOH.")
    else:
        reply = get_gemini_response(user_msg, report)
        st.success("AI Response")
        st.write(reply)

#streamlit styling
st.header("Linear Regression Model")

#threshold scaler
threshold = st.number_input(
    "SOH Fail Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.6,
    step=0.05
)

#make button for running the regression model
if st.button("Run SOH Prediction Model"):

    #create variables to be passed to regression model
    env = os.environ.copy()
    env["SOH_THRESHOLD"] = str(threshold)

    #streamlit styling
    with st.spinner("Running regression model..."):

        #runs the linear regression model with the defined executeable
        result = subprocess.run(
            [PYTHON_PATH, MODEL_PATH],
            cwd=BASE_DIR,
            env=env,
            capture_output=True,
            text=True,
            shell=False
        )

    #streamlit styling
    st.subheader("Model Output")
    st.code(result.stdout)

    #error handling
    if result.stderr:
        st.subheader("Model Errors")
        st.code(result.stderr)

    #plot loading
    if os.path.exists(PLOT_FILE):
        st.image(PLOT_FILE, caption="Predicted vs True SOH", use_container_width=True)
    else:
        st.warning("Plot file not found. Model may have failed.")

    #reload json after run
    if os.path.exists(REPORT_FILE):
        try:
            with open(REPORT_FILE, "r") as f:
                report = json.load(f)

            avg_soh = report["metrics"]["avg_soh"]
            pass_count = report["metrics"]["pass_count"]
            fail_count = report["metrics"]["fail_count"]

            st.success(f"SOH Loaded Successfully: {avg_soh:.4f}")
            st.caption(f"PASS: {pass_count} | FAIL: {fail_count}")

            st.subheader("Cell Pass / Fail Results")
            st.dataframe(report["cells"])

        except:
            st.error("battery_report.json exists but could not be read.")
    else:
        st.warning("battery_report.json not generated.")
