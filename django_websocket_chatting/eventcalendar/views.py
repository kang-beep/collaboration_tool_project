
from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

@login_required
def calendar_view(request):
    return render(request, 'calendar/calendar.html')
