# SOFE377U Final Project - Part 2: Linear Regression Model

This section of the project uses a linear regression model to predict the SOH of a battery pack based on 21 voltage readings. Using a threshold (configurable, with default 0.6), the model reads several clusters of battery pack values from the PulseBat dataset Excel file, evaluates the performance of the model using different metrics (R^2, MSE, MAE), and displays a table with true/predicted SOH and pass/fail results. The table values are plotted on a graph plotting the true SOH against the predicted SOH for visual comparison.

Execution Requirements:
- Python 3.8 or higher
- pandas
- scikit-learn
- matplotlib
- openpyxl

Execution Steps:
1. Download project foler
2. Install required libraries (see above)
3. Open project in IDE
4. Set the correct Python interpreter
5. Run the script
6. Enter an SOH threshold
7. View plotted results

Input Data:
- PulseBat Dataset.xlsx

SOFE 3370U – Final Project
Authors: Kyle S., Kaira S., Colton B., Vlad S., Nabhil I.
Ontario Tech University
Date: Oct. 23rd, 2025
