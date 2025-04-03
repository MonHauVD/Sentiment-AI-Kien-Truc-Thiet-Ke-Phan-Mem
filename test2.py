import keras

try:
    model = keras.models.load_model("deep_learning_model.h5")
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading model:", e)
