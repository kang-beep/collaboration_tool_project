
## 3rd-party
from rest_framework import serializers

## custom modules
from document_ocr.models import OCRRequestLog


class OCRSerializer(serializers.ModelSerializer):
    """
    OCR Serializer.

    """
    
    class Meta:
        model = OCRRequestLog
        fields = [
            # (쓰기용) 요청 데이터
            "image",

        ]
        
        extra_kwargs = {
            "image": {"write_only": True},

        }


    