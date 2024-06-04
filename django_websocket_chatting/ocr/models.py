from django.db import models

class OcrResult(models.Model):
    image = models.ImageField(upload_to='images/')
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
