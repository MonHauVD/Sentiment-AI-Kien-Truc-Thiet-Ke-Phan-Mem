from flask import Flask, jsonify, request
import mysql.connector
import os
import tensorflow as tf
import numpy as np
import joblib
import pandas as pd

app = Flask(__name__)

# Kết nối MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "12345678",
    "database": "review_db2"
}

# Đường dẫn lưu model
MODEL_PATH = "models/"

# Hàm kết nối MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

# API lấy thống kê dữ liệu từ database
@app.route("/api/data-distribution", methods=["GET"])
def get_data_distribution():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Truy vấn số lượng review theo phân loại
    query = """
    SELECT 
        SUM(CASE WHEN rating IN (1, 2) THEN 1 ELSE 0 END) AS negative,
        SUM(CASE WHEN rating = 3 THEN 1 ELSE 0 END) AS neutral,
        SUM(CASE WHEN rating IN (4, 5) THEN 1 ELSE 0 END) AS positive
    FROM reviews;
    """
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({"labels": ["Negative", "Neutral", "Positive"], "data": list(result)})
    return jsonify({"labels": ["Negative", "Neutral", "Positive"], "data": ["NA", "NA", "NA"]})

# Hàm train model nếu chưa có
def train_and_save_model(model_type):
    conn = get_db_connection()
    df = pd.read_sql("SELECT reviewText, rating FROM reviews", conn)
    conn.close()

    # Tiền xử lý dữ liệu
    df["label"] = df["rating"].apply(lambda x: 0 if x <= 2 else (1 if x == 3 else 2))
    X = df["reviewText"]
    y = df["label"]

    # Chuyển đổi text sang số
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(max_features=5000)
    X_transformed = vectorizer.fit_transform(X).toarray()

    # Lưu vectorizer
    joblib.dump(vectorizer, os.path.join(MODEL_PATH, "vectorizer.pkl"))

    # Tạo model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(3, activation="softmax")
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    # Train
    model.fit(X_transformed, y, epochs=5, batch_size=32, validation_split=0.2)

    # Lưu model
    model.save(os.path.join(MODEL_PATH, f"{model_type}.h5"))

    return model

# API lấy độ chính xác của các model
@app.route("/api/model-accuracy", methods=["GET"])
def get_model_accuracy():
    accuracies = {}
    for model_type in ["CNN", "RNN", "LSTM"]:
        model_file = os.path.join(MODEL_PATH, f"{model_type}.h5")
        if os.path.exists(model_file):
            model = tf.keras.models.load_model(model_file)
            accuracies[model_type] = round(np.random.uniform(80, 90), 2)  # Giả lập
        else:
            train_and_save_model(model_type)
            accuracies[model_type] = "Training"

    return jsonify({"labels": ["CNN", "RNN", "LSTM"], "data": [accuracies.get("CNN", "NA"), accuracies.get("RNN", "NA"), accuracies.get("LSTM", "NA")]})


if __name__ == "__main__":
    os.makedirs(MODEL_PATH, exist_ok=True)
    app.run(host="0.0.0.0", port=8000, debug=True)
