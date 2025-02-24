"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from home.views import front_view

urlpatterns = [
    
    #path('', front_view , name='home'),
    path('', RedirectView.as_view(pattern_name='accounts:login'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('home/', include('home.urls')),
    path('docsumm/', include('docsumm.urls')),
    path('eventcalendar/', include('eventcalendar.urls', namespace='eventcalendar')),
    path('teams/', include('teams.urls')),
    path('ocr/', include('ocr.urls')),
    path('stt/', include('stt.urls')),
    
    # path('', RedirectView.as_view(pattern_name="chat:index"), name="root"),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
