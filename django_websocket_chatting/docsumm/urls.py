from django.urls import path
from .views import *



app_name = "docsumm"

urlpatterns = [
    path("", generate_doc_summ, name="generate-doc-summ")
]
