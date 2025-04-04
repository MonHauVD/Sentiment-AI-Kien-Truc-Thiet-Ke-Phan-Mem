import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from .models import Review
import os

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        df = pd.read_csv(file)

        for _, row in df.iterrows():
            Review.objects.create(
                asin=row['asin'],
                helpful=row['helpful'],
                rating=row['rating'],
                review_text=row['reviewText'],
                review_time=row['reviewTime'],
                reviewer_id=row['reviewerID'],
                reviewer_name=row['reviewerName'],
                summary=row['summary'],
                unix_review_time=row['unixReviewTime']
            )
        return JsonResponse({'message': 'Upload thành công!'})
    return JsonResponse({'error': 'Lỗi khi upload'}, status=400)

from django.http import JsonResponse
from .train import train_model

def train(request, model_type):
    if model_type not in ['CNN', 'RNN', 'LSTM']:
        return JsonResponse({'error': 'Model không hợp lệ'}, status=400)

    message = train_model(model_type)
    return JsonResponse({'message': message})

from .predict import predict_review

def predict(request):
    if request.method == 'POST':
        review_text = request.POST.get('review')
        model_type = request.POST.get('model')

        if not review_text or not model_type:
            return JsonResponse({'error': 'Thiếu dữ liệu'}, status=400)

        result = predict_review(review_text, model_type)
        return JsonResponse({'prediction': result})
