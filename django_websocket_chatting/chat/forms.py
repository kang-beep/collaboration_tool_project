# chat/forms.py

from django import forms
from .models import Room, TeamMessage

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name"]

class TeamMessageForm(forms.ModelForm):
    class Meta:
        model = TeamMessage
        fields = ['message', 'image']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }
