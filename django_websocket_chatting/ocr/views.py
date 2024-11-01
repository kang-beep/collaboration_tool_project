import sys
import os
ocr_path = os.path.dirname(os.path.abspath(__file__))
if ocr_path not in sys.path:
    sys.path.append(ocr_path)

import cv2
import fitz
from docx import Document
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from pororo import Pororo
from pororo.pororo import SUPPORTED_TASKS
from utils.image_convert import convert_coord, crop
from utils.pre_processing import load_with_filter, roi_filter
from easyocr import Reader

class OCRView(View):
    def get(self, request):
        return render(request, 'ocr/upload.html')

    def post(self, request):
        if 'ocr_image' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'})

        uploaded_file = request.FILES['ocr_image']
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        file_extension = os.path.splitext(file_path)[1].lower()
        ocr_result = []

        if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
            image = load_with_filter(file_path)
            ocr_result = self.run_ocr(image)
        elif file_extension == '.pdf':
            ocr_result = self.handle_pdf(file_path)
        elif file_extension == '.docx':
            ocr_result = self.extract_text_from_docx(file_path)
        else:
            return JsonResponse({'error': '지원되지 않는 파일 형식입니다.'})

        return JsonResponse({'text': ocr_result, 'uploaded_file_url': file_path})

    def run_ocr(self, img_path):
        m_ocr = EasyPororoOcr()
        return m_ocr.run_ocr(img_path)

    def handle_pdf(self, pdf_path):
        pdf_document = fitz.open(pdf_path)
        result_text = []

        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img_path = f'output_page_{page_num}.png'
            pix.save(img_path)
            
            image = load_with_filter(img_path)
            result_text.append(f'OCR 결과값 (페이지 {page_num + 1}): {self.run_ocr(image)}')
            os.remove(img_path)  # 임시 파일 삭제

        return result_text

    def extract_text_from_docx(self, docx_file):
        doc = Document(docx_file)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return text

class EasyPororoOcr:
    def __init__(self, lang: list[str] = ["ko", "en"], gpu=False, **kwargs):
        self._detector = Reader(lang_list=lang, gpu=gpu, **kwargs).detect
        self._ocr = Pororo(task="ocr", lang="ko", model="brainocr", **kwargs)

    def create_result(self, points, img):
        roi = crop(img, points)
        result = self._ocr(roi_filter(roi))
        text = " ".join(result)
        return text

    def run_ocr(self, img_path):
        img = cv2.imread(img_path) if isinstance(img_path, str) else img_path
        detect_result = self._detector(img, slope_ths=0.3, height_ths=1)
        horizontal_list, free_list = detect_result
        rois = [convert_coord(point) for point in horizontal_list[0]] + free_list[0]
        ocr_results = [self.create_result(roi, img) for roi in rois]
        return ocr_results
