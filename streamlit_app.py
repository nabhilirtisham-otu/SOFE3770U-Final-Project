import streamlit as st
import subprocess
import os
import sys
from chatbot import get_gemini_response


#streamlit page styling
st.set_page_config(page_title="Battery Health AI", layout="centered")

#define files to used in the rest of the code 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "LinearRegressionModel.py")
PYTHON_PATH = sys.executable
SOH_FILE = os.path.join(BASE_DIR, "latest_soh.txt")
PLOT_FILE = os.path.join(BASE_DIR, "soh_plot.png")

#streamlit page styling
st.title("Battery Health Assistant")
st.caption("SOH Prediction + Gemini AI Advisor")
st.header("Battery Advisor")

#creates user input box 
user_msg = st.text_input("Ask about battery health, charging, lifespan, or safety:")

#initialize soh
soh_value = None

#open and read the soh file 
if os.path.exists(SOH_FILE):
    try:
        with open(SOH_FILE, "r") as f:
            soh_value = float(f.read().strip())
        st.metric("Predicted Battery SOH", f"{soh_value:.4f}") #print predicted SOH value
    except Exception as e:
        st.error(f"Error reading SOH file: {e}")

#handle user inputs with correct error handling
if st.button("Ask AI"):
    if user_msg.strip() == "":
        st.warning("Please enter a question.")
    elif soh_value is None:
        st.error("Run the model first to generate SOH.")
    else:
        reply = get_gemini_response(user_msg, soh_value)
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
    st.code(result.stdout) #prints all true and predicted SOH values as well as the status

    #error handling in case the regression model fails
    if result.stderr:
        st.subheader("Model Errors")
        st.code(result.stderr)

    
    #loads the plot.py into a picture and displays it
    if os.path.exists(PLOT_FILE):
        st.image(PLOT_FILE, caption="Predicted vs True SOH", use_container_width=True)
    else:
        st.warning("Plot file not found. Model may have failed.")

    
    #opens and reads the SOH file
    if os.path.exists(SOH_FILE):
        try:
            with open(SOH_FILE, "r") as f:
                soh_value = float(f.read().strip())
            st.success(f"SOH loaded successfully: {soh_value:.4f}") #prints SOH value
        except:
            st.error("SOH file exists but could not be read.")
    else:
        st.warning("SOH file not generated.")

#streamlit styling 
st.markdown("---")
st.caption("SOFE3770U Final Project | Battery Health AI")
