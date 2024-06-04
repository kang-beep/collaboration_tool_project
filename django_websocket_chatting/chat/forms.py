from django import forms
from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name"] # fields = ['name', 'description'] / description이 models.py에 없음