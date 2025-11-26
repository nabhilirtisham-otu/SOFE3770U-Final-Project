# SOFE377U Final Project - Part 2: Linear Regression Model

This project uses a linear regression model to predict the SOH of a battery pack based on 21 voltage readings. Using a threshold (configurable, with default 0.6), the model reads several clusters of battery pack values from the PulseBat dataset Excel file, evaluates the performance of the model using different metrics (R^2, MSE, MAE), and displays a table with true/predicted SOH and pass/fail results. The table values are plotted on a graph plotting the true SOH against the predicted SOH for visual comparison. It then exports this information where it is used by the gemini AI API. The project uses a streamlit frontend to display the information. 

Execution Requirements:
- Python 3.8 or higher
- pandas
- scikit-learn
- matplotlib
- openpyxl
- google-genai
- google-generativeai

Execution Steps:
1. Download project folder
2. Install required libraries using "pip install streamlit pandas scikit-learn matplotlib openpyxl python-dotenv google-generativeai google-genai" (see above)
3. Open project in IDE
4. Set the correct Python interpreter
5. Run the script using "python -m streamlit run streamlit_app.py in the terminal
6. Enter an SOH threshold
7. Press the run SOH prediction model button
8. View plotted results
9. Ask AI chatbot questions by typing in question and then pressing ask AI

Input Data:
- PulseBat Dataset.xlsx

SOFE 3370U – Final Project
Authors: Kyle S., Kaira S., Colton B., Vlad S., Nabhil I.
Ontario Tech University
Date: Oct. 23rd, 2025

https://github.com/nabhilirtisham-otu/SOFE3770U-Final-Project

<img width="911" height="1002" alt="image" src="https://github.com/user-attachments/assets/6215a2de-301d-4b20-82c7-811c53adaa6f" />


