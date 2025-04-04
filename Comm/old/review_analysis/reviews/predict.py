from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from .train import MAX_LEN, MAX_WORDS

tokenizer = None  # Load tokenizer từ train

def predict_review(review_text, model_type):
    global tokenizer

    if tokenizer is None:
        return "Hãy train model trước khi dự đoán."

    sequence = tokenizer.texts_to_sequences([review_text])
    padded = pad_sequences(sequence, maxlen=MAX_LEN)

    model = load_model(f'model_{model_type}.h5')
    prediction = model.predict(padded)
    
    labels = ['negative', 'neutral', 'positive']
    return labels[np.argmax(prediction)]
