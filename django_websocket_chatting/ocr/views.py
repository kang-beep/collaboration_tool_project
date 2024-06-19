import os
import warnings
import cv2
from abc import ABC, abstractmethod
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.files.storage import FileSystemStorage
# from pororo import Pororo
# from pororo.pororo import SUPPORTED_TASKS
# from utils.image_convert import convert_coord, crop
# from utils.pre_processing import load_with_filter, roi_filter
from easyocr import Reader
from docx import Document
import fitz


class BaseOcr(ABC):
    def __init__(self):
        self.img_path = None
        self.ocr_result = {}

    def get_ocr_result(self):
        return self.ocr_result

    def get_img_path(self):
        return self.img_path

    @abstractmethod
    def run_ocr(self, img_path: str, debug: bool = False):
        pass

class PororoOcr(BaseOcr):
    def __init__(self, model: str = "brainocr", lang: str = "ko", **kwargs):
        super().__init__()
        self._ocr = Pororo(task="ocr", lang=lang, model=model, **kwargs)

    def run_ocr(self, img_path: str, debug: bool = False):
        self.img_path = img_path
        self.ocr_result = self._ocr(img_path, detail=True)

        if self.ocr_result['description']:
            ocr_text = self.ocr_result["description"]
        else:
            ocr_text = "No text detected."

        return ocr_text

    @staticmethod
    def get_available_langs():
        return SUPPORTED_TASKS["ocr"].get_available_langs()

    @staticmethod
    def get_available_models():
        return SUPPORTED_TASKS["ocr"].get_available_models()

class EasyOcr(BaseOcr):
    def __init__(self, lang: list[str] = ["ko", "en"], gpu=False, **kwargs):
        super().__init__()
        self._ocr = Reader(lang_list=lang, gpu=gpu, **kwargs).readtext

    def run_ocr(self, img_path: str, debug: bool = False):
        self.img_path = img_path
        self.ocr_result = self._ocr(img_path, detail=1)

        if len(self.ocr_result) != 0:
            ocr_text = list(map(lambda result: result[1], self.ocr_result))
        else:
            ocr_text = "No text detected."

        return ocr_text

class EasyPororoOcr(BaseOcr):
    def __init__(self, lang: list[str] = ["ko", "en"], gpu=False, **kwargs):
        super().__init__()
        self._detector = Reader(lang_list=lang, gpu=gpu, **kwargs).detect
        self._ocr = Pororo(task="ocr", lang="ko", model="brainocr", **kwargs)

    def create_result(self, points):
        roi = crop(self.img, points)
        result = self._ocr(roi_filter(roi))
        text = " ".join(result)

        return text

    def run_ocr(self, img_path: str, debug: bool = False, **kwargs):
        self.img_path = img_path
        self.img = cv2.imread(img_path) if isinstance(img_path, str) \
            else self.img_path

        self.detect_result = self._detector(self.img, slope_ths=0.3, height_ths=1)

        horizontal_list, free_list = self.detect_result

        rois = [convert_coord(point) for point in horizontal_list[0]] + free_list[0]

        ocr_results = [self.create_result(roi) for roi in rois]

        return ocr_results

class OCRView(View):
    def get(self, request):
        return render(request, 'ocr/upload.html')

    def post(self, request):
        if 'ocr_image' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        ocr_image = request.FILES['ocr_image']
        fs = FileSystemStorage()
        filename = fs.save(ocr_image.name, ocr_image)
        uploaded_file_url = fs.url(filename)

        # 여기에 OCR 기능 통합 (PororoOcr, EasyOcr, EasyPororoOcr 중 하나 선택)
        m_ocr = EasyPororoOcr()
        text = m_ocr.run_ocr(fs.path(filename))

        return JsonResponse({'uploaded_file_url': uploaded_file_url, 'text': text})