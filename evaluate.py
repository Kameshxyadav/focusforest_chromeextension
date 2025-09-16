import pandas as pd
import joblib

# === Load model ===
model = joblib.load("stacked_model_old.pkl")

# === Create input row including 'index' and 'pl'
input_data = pd.DataFrame([{
    "PPG_Signal": 537.87,
    "Heart_Rate": 61.73,
    "Systolic_Peak": 554.41,
    "Diastolic_Peak": 516.08,
    "Pulse_Area": 536.68,
    "index": 0,
    "Gender": 1,
    "Age": 31,
    "Height": 154.94,
    "Weight": 53,
    "pl": 1
}])

# === Predict glucose level
predicted_glucose = model.predict(input_data)

# === Print prediction
print("🧪 Predicted Glucose Level:", round(predicted_glucose[0], 2))
