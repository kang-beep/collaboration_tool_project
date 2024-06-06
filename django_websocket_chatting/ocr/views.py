# ocr/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.files.storage import FileSystemStorage

class OCRView(View):
    def get(self, request):
        return render(request, 'ocr/upload.html')
    def post(self, request):
        if request.method == 'POST' and request.FILES.get('ocr_image'):
            ocr_image = request.FILES['ocr_image']
            fs = FileSystemStorage()
            filename = fs.save(ocr_image.name, ocr_image)
            uploaded_file_url = fs.url(filename)
            # 여기서 OCR 함수를 호출하여 파일을 처리합니다
            # 예: text = your_ocr_function(fs.path(filename))
            text = "Sample OCR Result"  # 임시 텍스트
            return JsonResponse({'uploaded_file_url': uploaded_file_url, 'text': text})
        return JsonResponse({'error': 'No file uploaded'}, status=400)

