from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
# Load dataset
df = pd.read_csv("all_kindle_review.csv")
df = df[['reviewText', 'rating']].dropna()

def label_sentiment(rating):
    if rating in [1, 2]: return "negative"
    elif rating == 3: return "neutral"
    else: return "positive"

df['sentiment'] = df['rating'].apply(label_sentiment)

# Tokenizer setup
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(df['reviewText'])

def preprocess_text(text):
    sequences = tokenizer.texts_to_sequences([text])
    return pad_sequences(sequences, maxlen=200)

# Load models
models = {
    "cnn": tf.keras.models.load_model("models/cnn_model.h5"),
    "rnn": tf.keras.models.load_model("models/rnn_model.h5"),
    "lstm": tf.keras.models.load_model("models/lstm_model.h5")
}



# Data distribution
@app.route("/dataDistribution", methods=["GET"])
def data_distribution():
    distribution = df['sentiment'].value_counts().to_dict()
    print("data_distribution: ",distribution)
    return jsonify(distribution)

# Model accuracy comparison
@app.route("/accuracyComparison", methods=["GET"])
def accuracy_comparison():
    # # Lấy tập test từ DataFrame
    # sample_df = df.sample(n=10000, random_state=42)

    # # Lấy dữ liệu và label
    # test_texts = sample_df["reviewText"].values
    # test_labels = sample_df["rating"].apply(lambda x: 2 if x in [4, 5] else (0 if x in [1, 2] else 1)).values

    # # Tiền xử lý dữ liệu văn bản
    # test_texts = np.array([preprocess_text(text) for text in test_texts])
    # test_texts = test_texts.squeeze(axis=1) 

    # # Đánh giá từng model
    # accuracy = {
    #     "cnn": models["cnn"].evaluate(test_texts, test_labels, verbose=0)[1],  # Độ chính xác CNN
    #     "rnn": models["rnn"].evaluate(test_texts, test_labels, verbose=0)[1],  # Độ chính xác RNN
    #     "lstm": models["lstm"].evaluate(test_texts, test_labels, verbose=0)[1],  # Độ chính xác LSTM
    # }

    accuracy = {'cnn': 0.9383999705314636, 'rnn': 0.8095999956130981, 'lstm': 0.9172999858856201}
    print("accuracy_comparison: ", accuracy)
    return jsonify(accuracy)

# Predict review sentiment
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data.get("review", "")
    print("text: ", text)
    model_type = data.get("model", "cnn")
    print("model_type: ", model_type)
    processed_text = preprocess_text(text)
    prediction = models[model_type].predict(processed_text)
    sentiment = ["negative", "neutral", "positive"]
    result = sentiment[np.argmax(prediction)]
    print("predict: ", result)
    return jsonify({"predicted_sentiment": result})

df2 = pd.read_csv("all_kindle_review.csv")

# Chuẩn bị sample reviews
def get_sample_reviews():
    sample = df2[["reviewText", "rating"]].dropna().sample(100).to_dict(orient="records")
    for review in sample:
        review["sentiment"] = "negative" if review["rating"] in [1, 2] else "neutral" if review["rating"] == 3 else "positive"
    return sample

@app.route("/sampleReviews", methods=["GET"])
def sample_reviews():
    return jsonify(get_sample_reviews())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
