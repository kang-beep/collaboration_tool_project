import cv2
from abc import ABC, abstractmethod
from pororo import Pororo
from pororo.pororo import SUPPORTED_TASKS
from utils.image_convert import convert_coord, crop
from utils.pre_processing import load_with_filter, roi_filter
from easyocr import Reader
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
    image_path = input("이미지 경로 입력: ")

    image = load_with_filter(image_path)

    text = m_ocr.run_ocr(image)
    print('OCR 결과값:', text)
