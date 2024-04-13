from django.db import models


class OCRRequestLog(models.Model):
    # (Request) 요청 데이터
    image = models.ImageField(blank=False, null=False, upload_to="document_ocr/%Y-%m-%d/")  # 이미지 파일
    
    # (Response) 응답 데이터
    result = models.TextField()  # OCR 결과 시간
    
    ## 로그기록용
    requested_at = models.DateTimeField(auto_now_add=True)  # API 요청시간
    requested_ip = models.CharField(max_length=50)
    requested_user = models.CharField(max_length=50)
    
