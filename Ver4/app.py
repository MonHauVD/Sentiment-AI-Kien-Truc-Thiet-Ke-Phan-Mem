from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
app = Flask(__name__)
# Load trained model
model = tf.keras.models.load_model("diabetes_model.h5")
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)[0][0]
    result = "Diabetic" if prediction > 0.5 else "Non-Diabetic"
    return jsonify({"prediction": result, "probability": float(prediction)})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)