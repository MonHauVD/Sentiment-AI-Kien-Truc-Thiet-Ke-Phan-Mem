from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
import joblib
from flask_cors import CORS

# Load model and scaler
model = tf.keras.models.load_model("diabetes_model.h5")
scaler = joblib.load("scaler.pkl")

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate

# Route to serve the frontend
@app.route("/")
def home():
    return render_template("index.html")

# Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json  # Get JSON input
        features = np.array(data["features"]).reshape(1, -1)  # Convert to array
        scaled_features = scaler.transform(features)  # Scale features
        prediction = model.predict(scaled_features)[0][0]  # Get prediction
        result = "Diabetic" if prediction > 0.5 else "Not Diabetic"
        return jsonify({"prediction": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)
