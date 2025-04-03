import streamlit as st
import numpy as np
import joblib
import keras
from sklearn.preprocessing import StandardScaler

# Load trained models and scaler
scaler = joblib.load("scaler.pkl")
models = {
    "kNN": joblib.load("knn_model.pkl"),
    "SVM Linear": joblib.load("svm_linear_model.pkl"),
    "SVM RBF": joblib.load("svm_rbf_model.pkl"),
    "Logistic Regression": joblib.load("logistic_regression_model.pkl"),
    "Deep Learning": keras.models.load_model("deep_learning_model.h5")
}

# Define input fields
st.title("Diabetes Prediction App")
st.write("Enter patient details to predict diabetes using different models.")

features = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
]
user_input = [st.number_input(f, value=0.0) for f in features]
model_choice = st.selectbox("Select a Model", list(models.keys()))

if st.button("Predict"):
    user_input_scaled = scaler.transform([user_input])
    
    if model_choice == "Deep Learning":
        prediction = (models[model_choice].predict(user_input_scaled) > 0.5).astype(int)
    else:
        prediction = models[model_choice].predict(user_input_scaled)
    
    st.write("Prediction:", "Diabetic" if prediction[0] else "Not Diabetic")
