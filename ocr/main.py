import cv2
from abc import ABC, abstractmethod
from pororo import Pororo
from pororo.pororo import SUPPORTED_TASKS
from utils.image_convert import convert_coord, crop
from utils.pre_processing import load_with_filter, roi_filter
from easyocr import Reader
from docx import Document
import fitz
import os
import warnings

warnings.filterwarnings('ignore')

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

if __name__ == "__main__":
    m_ocr = EasyPororoOcr()
    input_path = input("이미지 경로 입력: ")
    file_extension = os.path.splitext(input_path)[1].lower()

    if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
        image = load_with_filter(input_path)
        text = m_ocr.run_ocr(image)
        print('OCR 결과값:', text)
        
    elif file_extension == '.pdf':
        pdf_document = fitz.open(input_path)
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img_path = f'output_page_{page_num}.png'
            pix.save(img_path)
            
            image = load_with_filter(img_path)
            text = m_ocr.run_ocr(image)
            print(f'OCR 결과값 (페이지 {page_num + 1}):', text)
            os.remove(img_path)  # 임시 파일 삭제 # 바뀐 이미지 확인 원할경우 해당 코드 삭제
    
    elif file_extension == '.docx':
        def extract_text_from_docx(docx_file):
            doc = Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text

        # DOCX 파일의 텍스트 추출
        text = extract_text_from_docx(input_path)

        # 추출된 텍스트 출력
        print(text)
        
    else:
        print("지원되지 않는 파일 형식입니다. (pdf or 이미지 파일만 지원가능)")
