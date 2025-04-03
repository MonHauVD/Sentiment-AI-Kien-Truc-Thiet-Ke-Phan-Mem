import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
# Load dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
"BMI", "DiabetesPedigreeFunction", "Age", "Outcome"]
df = pd.read_csv(url, names=columns)
# Split features and target
X = df.drop("Outcome", axis=1)
y = df["Outcome"]# Normalize input features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
# Build deep learning model
def create_model():
    model = Sequential([
    Dense(128, activation="relu", input_shape=(X_train.shape[1],)), Dropout(0.3),
    Dense(64, activation="relu"), Dropout(0.3),
    Dense(32, activation="relu"),
    Dense(16, activation="relu"),
    Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model
# Train model
model = create_model()
model.fit(X_train, y_train, epochs=100, batch_size=10, validation_data=(X_test, y_test))
# Save model and scaler
model.save("diabetes_model.h5")
joblib.dump(scaler, "scaler.pkl")
print("Model and scaler saved successfully!")