from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
import joblib
# Load model and scaler
model = tf.keras.models.load_model("diabetes_model.h5")
scaler = joblib.load("scaler.pkl")
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        try:
        # Get input values from form
            features = [float(request.form[f]) for f in ["Pregnancies", "Glucose", "BloodPressure",
            "SkinThickness", "Insulin", "BMI",
            "DiabetesPedigreeFunction", "Age"]]
            # Scale input
            input_data = scaler.transform([features])# Predict
            pred_prob = model.predict(input_data)[0][0]
            prediction = "Diabetic" if pred_prob > 0.5 else "Not Diabetic"
        except Exception as e:
         prediction = f"Error: {e}"
    return render_template("index.html", prediction=prediction)
if __name__ == "__main__":
    app.run(debug=True)