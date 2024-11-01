from django.urls import path
from .views import *
from .api.docsumm_api import DocSummAPIView


app_name = "docsumm"

urlpatterns = [
    path("", generate_doc_summ, name="generate-doc-summ"),
    
    ## api
    path("api/docsumm/", DocSummAPIView.as_view(), name="api-docsumm"),
]
