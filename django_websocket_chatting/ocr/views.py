from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import OcrForm
from .models import OcrResult
from .utils import EasyPororoOcr
import os

def index(request):
    if request.method == 'POST':
        form = OcrForm(request.POST, request.FILES)
        if form.is_valid():
            ocr_instance = form.save()
            ocr = EasyPororoOcr()
            img_path = ocr_instance.image.path
            result = ocr.run_ocr(img_path)
            ocr_instance.result = "\n".join(result)
            ocr_instance.save()
            return redirect('result', pk=ocr_instance.pk)
    else:
        form = OcrForm()
    return render(request, 'ocr/index.html', {'form': form})

def result(request, pk):
    ocr_instance = OcrResult.objects.get(pk=pk)
    return render(request, 'ocr/result.html', {'ocr_instance': ocr_instance})
