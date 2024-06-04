from django import forms
from .models import OcrResult

class OcrForm(forms.ModelForm):
    class Meta:
        model = OcrResult
        fields = ['image']
