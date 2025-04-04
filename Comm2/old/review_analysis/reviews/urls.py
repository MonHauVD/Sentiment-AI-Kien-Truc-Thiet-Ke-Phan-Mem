from django.urls import path
from .views import upload_csv, train, predict

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('train/<str:model_type>/', train, name='train'),
    path('predict/', predict, name='predict'),
]
