"""
## 개요
    싱글톤 패턴으로 구현된 토크나이저 및 모델 로더.
    실제로 필요할 때, 토큰 및 모델 객체를 반환하게 해줌으로써,
    Django 리로딩 시간 및 views 렌더링 시간을 줄임.

## 사용법
    from docsumm.utils.lazy_loader import LazyLoader

    model_loader = LazyLoader()
    model = model_loader.get_model()
    tokenizer = model_loader.get_tokenizer()

"""

import torch
from transformers import (
    PreTrainedTokenizerFast, BartForConditionalGeneration,
    BertTokenizer, BertModel
)

class LazyLoader():
    """
    싱글톤 패턴으로 구현된 토크나이저 및 모델 로더.
    실제로 필요할 때, 토크나이저 및 모델 객체를 반환하게 해줌으로써,
    Django 리로딩 시간 및 views 렌더링 시간을 줄임.
    
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LazyLoader, cls).__new__(cls)
            
            ## Abstractive Summary.
            cls._instance.kobart_tokenizer = None
            cls._instance.kobart_model = None
            
            ## Extractive Summary.
            cls._instance.kobert_tokenizer = None
            cls._instance.kobert_model = None

        return cls._instance


    def get_kobart_tokenizer(self):
        """
        싱글톤으로 이루어진 KoBART 토크나이저 객체 반환.
    
        Returns:
            - 토크나이저 객체 반환.
            
        """
        if self.kobart_tokenizer is None:
            self.kobart_tokenizer = PreTrainedTokenizerFast.from_pretrained("EbanLee/kobart-summary-v3")
            
        return self.kobart_tokenizer


    def get_kobart_model(self):
        """
        싱글톤으로 이루어진 KoBART 모델 객체 반환.
    
        Returns:
            - 토크나이저 객체 반환.
            
        """
        if self.kobart_model is None:
            self.kobart_model = BartForConditionalGeneration.from_pretrained("EbanLee/kobart-summary-v3")
            self.kobart_model.eval()  # 추론 모드로 설정
            
        return self.kobart_model


    def get_kobert_tokenizer(self):
        """
        싱글톤으로 이루어진 KoBert 모델 객체 반환.
    
        Returns:
            - 토크나이저 객체 반환.
            
        """        
        if self.kobert_tokenizer is None:
            self.kobert_tokenizer = BertTokenizer.from_pretrained("monologg/kobert")
            
        return self.kobert_tokenizer


    def get_kobert__model(self):
        """
        싱글톤으로 이루어진 KoBert 모델 객체 반환.
    
        Returns:
            - 토크나이저 객체 반환.
            
        """        
        if self.kobert_model is None:
            self.kobert_model = BertModel.from_pretrained("monologg/kobert")
            self.kobert_model.eval()  # 추론 모드로 설정
            
        return self.kobert_model




"""


"""