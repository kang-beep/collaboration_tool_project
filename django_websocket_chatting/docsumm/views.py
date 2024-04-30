from django.shortcuts import render
from django.http import HttpRequest



def generate_doc_summ(request: HttpRequest):
    return render(request, "docsumm/generate_doc_summ.html")