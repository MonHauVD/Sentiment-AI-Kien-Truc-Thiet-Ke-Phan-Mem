from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os


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
def data_distribution():
    distribution = df['sentiment'].value_counts().to_dict()
    print("data_distribution: ",distribution)
    # return jsonify(distribution)

# Model accuracy comparison
def accuracy_comparison():
    accuracy = {
        "cnn": models["cnn"].evaluate(preprocess_text(df['reviewText'][0]), np.array([1]))[1],
        "rnn": models["rnn"].evaluate(preprocess_text(df['reviewText'][0]), np.array([1]))[1],
        "lstm": models["lstm"].evaluate(preprocess_text(df['reviewText'][0]), np.array([1]))[1],
    }
    print("accuracy_comparison: ", accuracy)
    # return jsonify(accuracy)


def predict(text, model_type):
    processed_text = preprocess_text(text)
    prediction = models[model_type].predict(processed_text)
    sentiment = ["negative", "neutral", "positive"]
    result = sentiment[np.argmax(prediction)]
    print("predict: ", result)
    # return jsonify({"predicted_sentiment": result})



if __name__ == "__main__":
    # data_distribution()
    # accuracy_comparison()
    predict("I love this book", "cnn")
    predict("I love this book", "rnn")
    predict("Great short read.  I didn't want to put it down so I read it all in one sitting.  The sex scenes were great between the two males and one female character...a bit surprising - I never thought you could do that!  I learned something new and really enjoyed reading this book!  This is a great way to get all hot and bothered and take advantage of your significant other(s)!", "lstm")
