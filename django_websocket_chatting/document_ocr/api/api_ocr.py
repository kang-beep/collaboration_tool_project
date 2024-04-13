## built-in
import base64
from datetime import datetime

## 3rd-party
# django
from django.http import HttpRequest, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import APIException, ValidationError, MethodNotAllowed

# ocr stuff
import numpy as np
from pytesseract import Output
import pytesseract
import cv2

## custom modules
from document_ocr.serializers import *
from document_ocr.models import *



class OCRView(APIView):
    """
    OCR API View.
    
    """
    
    ## NOTE 인증된 사용자만 요청할 수 있게끔하려면 사용할 것.
    # authentication_classes = [TokenAuthentication]
    # permission_classes = []
    
    
    ## Overrides
    
    def handle_exception(self, exc: APIException) -> HttpResponse:
        """
        API 반환 시, 커스텀 메시지
        
        """
        
        
        if isinstance(exc, ValidationError):
            """
            Serializers 에러. 필드 누락 에러 등.
            """
            
            response_data = {
                "message": "이미지가 없습니다. 다시 확인하고 요청해주세요."
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        
        if isinstance(exc, MethodNotAllowed):
            """
            작성되어 있지 않은 API 포인트로 요청시 에러.
            """
            
            response_data = {
                "message": "이 endpoint에서 해당 method는 지원하지 않습니다."
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        
        return super().handle_exception(exc)
    
    
    
    def get_client_ip(self, request: HttpRequest) -> str:
        """
        요청 ip 주소 추출
        
        Args:
            - request (HttpRequest): Http Request 정보
        
        Returns:
            - (str): ip 주소 반환
        """
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # X-Forwarded-For의 첫 번째 주소가 실제 클라이언트 IP
            
        else:
            ip = request.META.get('REMOTE_ADDR')  # 직접 연결된 경우
            
        return ip
    
    ## custom functions.
    def do_ocr(self, src_image: bytes) -> tuple:
        """
        이미지를 받아 OCR 수행
        
        Args:
            - src_iamge (str): base64로 인코딩된 문자열
        
        Returns:
            str: tesseract OCR 추론 결과.
            datetime.timedelta: tesseract OCR 추론 소요시간
            
        """
        
        
        # base64 decode
        nparr = np.frombuffer(src_image, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        
        ## (선택) 이미지 전처리 
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # (선택) 흑백으로 변환
        img = cv2.medianBlur(img, 5)  # (선택) 중간값 블러를 사용하여 잡음 제거
        
        result = pytesseract.image_to_string(image=img, lang="kor+eng")
        
        
        return result
    
    
    
    def post(self, request:HttpRequest) -> HttpResponse:
        """
        JSON 형식의 OCR 추론 결과 반환.
        
        Args:
            - request (HttpRequest): HTTP 요청.
        
        Returns:
            - HttpResonse: Json 형식의 HttpResponse 반환.
            
        """
        requested_at = datetime.now()
        
        serializer = OCRSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            validated_image = serializer.validated_data.get("image")
            
            print(f"{validated_image = }")
            result = self.do_ocr(validated_image.read())
            
            requested_ip = self.get_client_ip(request)
            
            ## DB 저장
            OCRRequestLog.objects.create(
                image=validated_image,
                result=result,
                
                requested_at=requested_at,
                requested_ip=requested_ip,
                requested_user=request.user,
            )
            
            response_data = {
                "message": "OCR 성공!",
                "result": result,
            }
            
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        

