import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, LSTM, SimpleRNN, Dense, GlobalMaxPooling1D, Dropout
import os

# Đọc dữ liệu
df = pd.read_csv("all_kindle_review.csv")
df = df[['reviewText', 'rating']].dropna()

def label_sentiment(rating):
    if rating in [1, 2]:
        return 0  # Negative
    elif rating == 3:
        return 1  # Neutral
    else:
        return 2  # Positive

df['sentiment'] = df['rating'].apply(label_sentiment)

# Tiền xử lý văn bản
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(df['reviewText'])
sequences = tokenizer.texts_to_sequences(df['reviewText'])
X = pad_sequences(sequences, maxlen=200)
y = np.array(df['sentiment'])

# Chia tập train và test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Định nghĩa mô hình CNN
def create_cnn_model():
    model = Sequential([
        Embedding(10000, 128, input_length=200),
        Conv1D(128, 5, activation='relu'),
        GlobalMaxPooling1D(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(3, activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Định nghĩa mô hình RNN
def create_rnn_model():
    model = Sequential([
        Embedding(10000, 128, input_length=200),
        SimpleRNN(128, return_sequences=True),
        SimpleRNN(128),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(3, activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Định nghĩa mô hình LSTM
def create_lstm_model():
    model = Sequential([
        Embedding(10000, 128, input_length=200),
        LSTM(128, return_sequences=True),
        LSTM(128),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(3, activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Huấn luyện và lưu mô hình
os.makedirs("models", exist_ok=True)

print("Training CNN Model...")
cnn_model = create_cnn_model()
cnn_model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
cnn_model.save("models/cnn_model.h5")

print("Training RNN Model...")
rnn_model = create_rnn_model()
rnn_model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
rnn_model.save("models/rnn_model.h5")

print("Training LSTM Model...")
lstm_model = create_lstm_model()
lstm_model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
lstm_model.save("models/lstm_model.h5")

print("Training complete. Models saved in 'models/' folder.")
