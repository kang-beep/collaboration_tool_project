# calendar/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event')

app_name = 'eventcalendar'

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('api/', include(router.urls)),
]
