import tensorflow as tf
import numpy as np
import re
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load models
models = {
    "cnn": tf.keras.models.load_model("models/cnn_model.h5"),
    "rnn": tf.keras.models.load_model("models/rnn_model.h5"),
    "lstm": tf.keras.models.load_model("models/lstm_model.h5")
}


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

def accuracy_comparison():
    # Lấy tập test từ DataFrame
    sample_df = df.sample(n=10000, random_state=42)

    # Lấy dữ liệu và label
    test_texts = sample_df["reviewText"].values
    test_labels = sample_df["rating"].apply(lambda x: 2 if x in [4, 5] else (0 if x in [1, 2] else 1)).values

    # Tiền xử lý dữ liệu văn bản
    test_texts = np.array([preprocess_text(text) for text in test_texts])
    test_texts = test_texts.squeeze(axis=1) 

    # Đánh giá từng model
    accuracy = {
        "cnn": models["cnn"].evaluate(test_texts, test_labels, verbose=0)[1],  # Độ chính xác CNN
        "rnn": models["rnn"].evaluate(test_texts, test_labels, verbose=0)[1],  # Độ chính xác RNN
        "lstm": models["lstm"].evaluate(test_texts, test_labels, verbose=0)[1],  # Độ chính xác LSTM
    }

    print("accuracy_comparison: ", accuracy)
if __name__ == "__main__":
    accuracy_comparison()

