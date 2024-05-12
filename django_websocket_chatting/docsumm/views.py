from django.shortcuts import render, redirect
from django.http import HttpRequest



def generate_doc_summ(request: HttpRequest):
    """
    문서 요약 하는 페이지
    
    """
    
    return render(request, "docsumm/generate_doc_summ.html")
