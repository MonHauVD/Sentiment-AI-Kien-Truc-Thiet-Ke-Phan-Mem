from django.db import models

class Review(models.Model):
    asin = models.CharField(max_length=20)
    helpful = models.CharField(max_length=50)
    rating = models.IntegerField()
    review_text = models.TextField()
    review_time = models.CharField(max_length=50)
    reviewer_id = models.CharField(max_length=50)
    reviewer_name = models.CharField(max_length=100)
    summary = models.TextField()
    unix_review_time = models.BigIntegerField()

    def __str__(self):
        return f"{self.reviewer_name}: {self.summary}"

