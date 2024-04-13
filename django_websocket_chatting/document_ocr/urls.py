## 3rd-party
from django.urls import path

## custom modules
from document_ocr.api import *

app_name = "chat"

urlpatterns = [
    path("api/ocr/", OCRView.as_view(), name="api-ocr"),
    
]
