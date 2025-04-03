
import keras
import numpy as np
Deep_Learning_model= keras.models.load_model("deep_learning_model.h5")

data_test = np.array([[0, 100, 80, 20, 30, 25.5, 0.5, 30]])
print(Deep_Learning_model.predict(data_test))
