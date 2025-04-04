import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Conv1D, MaxPooling1D, Flatten
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from .models import Review

MAX_WORDS = 10000
MAX_LEN = 200

def preprocess_data():
    reviews = list(Review.objects.all().values('review_text', 'rating'))
    texts = [r['review_text'] for r in reviews]
    labels = [0 if r['rating'] <= 2 else 1 if r['rating'] == 3 else 2 for r in reviews]

    tokenizer = Tokenizer(num_words=MAX_WORDS)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    X = pad_sequences(sequences, maxlen=MAX_LEN)
    y = np.array(labels)

    return train_test_split(X, y, test_size=0.2), tokenizer

def create_model(model_type):
    model = Sequential()
    model.add(Embedding(MAX_WORDS, 128, input_length=MAX_LEN))
    
    if model_type == 'CNN':
        model.add(Conv1D(64, 5, activation='relu'))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Flatten())
    elif model_type == 'RNN':
        model.add(tf.keras.layers.SimpleRNN(128))
    elif model_type == 'LSTM':
        model.add(LSTM(128, return_sequences=True))
        model.add(LSTM(128))

    model.add(Dense(64, activation='relu'))
    model.add(Dense(3, activation='softmax'))

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train_model(model_type):
    (X_train, X_test, y_train, y_test), tokenizer = preprocess_data()
    model = create_model(model_type)
    
    model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_test, y_test))
    model.save(f'model_{model_type}.h5')

    return f"Model {model_type} đã được huấn luyện thành công!"
