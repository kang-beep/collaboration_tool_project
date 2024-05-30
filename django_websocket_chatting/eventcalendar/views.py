
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response  

from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(user=user)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        print(f"New event created: {instance.title}, {instance.start_time}, {instance.end_time}")
        
    
        
        
@login_required
def calendar_view(request):
    return render(request, 'calendar/calendar.html')
