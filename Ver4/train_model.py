import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import AdamW
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
# Load dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI",
"DiabetesPedigreeFunction", "Age", "Outcome"]
df = pd.read_csv(url, names=columns)
# Split data
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Normalize data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
# Build improved deep learning model
def create_model():
    model = Sequential([
    Dense(128, input_shape=(X_train.shape[1],)),
    BatchNormalization(),
    tf.keras.layers.LeakyReLU(alpha=0.1),
    Dropout(0.4),
    Dense(64),
    BatchNormalization(),
    tf.keras.layers.LeakyReLU(alpha=0.1),
    Dropout(0.3),
    Dense(32),
    BatchNormalization(),
    tf.keras.layers.LeakyReLU(alpha=0.1),
    Dense(16, activation="relu"),
    Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer=AdamW(learning_rate=0.001), loss="binary_crossentropy",
    metrics=["accuracy"])
    return model
# Train the model
model = create_model()
early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=10,
restore_best_weights=True)
model.fit(X_train, y_train, epochs=100, validation_data=(X_test, y_test), batch_size=16,
callbacks=[early_stopping])# Save the model
model.save("diabetes_model.h5")