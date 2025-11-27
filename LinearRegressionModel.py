import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import os
import json

# Show full tables
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# Load dataset
file_path = "PulseBat Dataset.xlsx"
df = pd.read_excel(file_path, sheet_name="SOC ALL")

# Inputs and target
X = df[[f"U{i}" for i in range(1, 22)]]
y = df["SOH"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Metrics
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print("\nMODEL EVALUATION METRICS")
print(f"R² Score: {r2:.4f}")
print(f"MSE: {mse:.4f}")
print(f"MAE: {mae:.4f}")

# Feature importance
coefficients = pd.Series(model.coef_, index=X.columns)
coeff_sorted = coefficients.reindex(coefficients.abs().sort_values(ascending=False).index)

print("\nFEATURE IMPORTANCE")
print(coeff_sorted)

# Threshold from environment
threshold_str = os.getenv("SOH_THRESHOLD", "0.6")
try:
    threshold = float(threshold_str)
except:
    threshold = 0.6

print(f"\nACTIVE THRESHOLD: {threshold}")

# Pass / Fail
status = ["fail" if soh < threshold else "pass" for soh in y_pred]

results = pd.DataFrame({
    "true soh": y_test.values,
    "predicted soh": y_pred,
    "status": status
})

print("\nBATTERY PACK RESULTS")
print(results)

num_pass = results["status"].value_counts().get("pass", 0)
num_fail = results["status"].value_counts().get("fail", 0)

print(f"\nSUMMARY: {num_pass} PASS, {num_fail} FAIL")

# Plot
plt.figure(figsize=(6, 6))
plt.scatter(y_test, y_pred, alpha=0.7, edgecolors="k")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--")
plt.xlabel("True SOH")
plt.ylabel("Predicted SOH")
plt.title("Linear Regression SOH Prediction")
plt.grid(True)
plt.savefig("soh_plot.png") #save plot to be passed to streamlit
plt.close()


#make json report for chatbot so data can be passed 
report = {
    "metrics": {
        "r2": float(r2),
        "mse": float(mse),
        "mae": float(mae),
        "threshold": float(threshold),
        "avg_soh": float(y_pred.mean()),
        "pass_count": int(num_pass),
        "fail_count": int(num_fail)
    },
    "cells": results.to_dict(orient="records"),
    "feature_importance": coeff_sorted.to_dict()
}

with open("battery_report.json", "w") as f:
    json.dump(report, f, indent=4)

print("\nCHATBOT DATA FILE CREATED: battery_report.json")
