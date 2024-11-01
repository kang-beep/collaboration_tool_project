from django.urls import path
from home import views

app_name = "home"

urlpatterns = [
    path("front", views.front_view, name='front'),
    path("main", views.index, name='main'),
]