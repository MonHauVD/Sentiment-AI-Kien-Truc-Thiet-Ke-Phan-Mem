import os 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' # hide warning
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow INFO and WARNING messages

import joblib  
import keras
import numpy as np
scaler = joblib.load("scaler.pkl")
knn_model = joblib.load("knn_model.pkl")  
SVM_Linear_model= joblib.load("svm_linear_model.pkl")
SVM_RBF_model= joblib.load("svm_rbf_model.pkl")
Logistic_Regression_model= joblib.load("logistic_regression_model.pkl")
Deep_Learning_model= keras.models.load_model("deep_learning_model.h5")

data_test = np.array([[10,139,80,0,0,27.1,1.441,57]]).reshape(1, -1)
data_test = scaler.transform(data_test)
print(knn_model.predict(data_test))
print(SVM_Linear_model.predict(data_test))
print(SVM_RBF_model.predict(data_test))
print(Logistic_Regression_model.predict(data_test))
print(Deep_Learning_model.predict(data_test))

while True:
    s = input("Enter 'e' to exit: ")
    if s == 'e':
        break
    else:
        arr = [float(x) for x in s.split(",")]
        data_test2 = np.array([arr]).reshape(1, -1)
        data_test2 = scaler.transform(data_test2)
        print(data_test2)
        print(knn_model.predict(data_test2))
        print(SVM_Linear_model.predict(data_test2))
        print(SVM_RBF_model.predict(data_test2))
        print(Logistic_Regression_model.predict(data_test2))
        print(Deep_Learning_model.predict(data_test2))
        
