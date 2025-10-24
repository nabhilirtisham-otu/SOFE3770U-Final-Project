import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# show full tables when printing so nothing gets cut off
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# load the dataset from excel
file_path = "SOFE3770U-Final-Project-main/PulseBat Dataset.xlsx"
df = pd.read_excel(file_path, sheet_name="SOC ALL")

# pick u1 to u21 as input features and soh as what we want to predict
X = df[[f"U{i}" for i in range(1, 22)]]
y = df["SOH"]

# split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# make the linear regression model and train it
model = LinearRegression()
model.fit(X_train, y_train)

# use the model to predict soh on the test set
y_pred = model.predict(X_test)

# calculate how well the model did using a few metrics
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print("\nmodel evaluation metrics:")
print(f"r² score: {r2:.4f}")
print(f"mean squared error (mse): {mse:.4f}")
print(f"mean absolute error (mae): {mae:.4f}")

# check which cells (u1-u21) have the biggest impact on soh
coefficients = pd.Series(model.coef_, index=X.columns)
coeff_sorted = coefficients.reindex(coefficients.abs().sort_values(ascending=False).index)
print("\nfeature importance (sorted by absolute magnitude):")
print(coeff_sorted)

# ask the user for the soh threshold (default is 0.6)
threshold = float(input("\nenter soh threshold (default 0.6): ") or 0.6)

# mark each battery as pass or fail based on the threshold
status = ["fail" if soh < threshold else "pass" for soh in y_pred]

# make a table with true soh, predicted soh, and pass/fail
results = pd.DataFrame({
    "true soh": y_test.values,
    "predicted soh": y_pred,
    "status": status
})

print("\nbattery pack test results:")
print(results)

# quick summary of how many passed and failed
num_pass = results["status"].value_counts().get("pass", 0)
num_fail = results["status"].value_counts().get("fail", 0)
print(f"\nsummary: {num_pass} pass, {num_fail} fail (threshold = {threshold})")

# plot the true soh vs predicted soh to see how close the model got
plt.figure(figsize=(6,6))
plt.scatter(y_test, y_pred, alpha=0.7, edgecolors="k")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--")
plt.xlabel("true soh")
plt.ylabel("predicted soh")
plt.title("linear regression soh prediction")
plt.grid(True)
plt.show()
