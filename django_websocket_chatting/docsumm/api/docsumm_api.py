## 3rd-party
from django.http import HttpRequest, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

## custom-modules
from docsumm.utils.do_abssumm import do_abssumm
from docsumm.utils.do_keywordext import do_keywordext



class DocSummAPIView(APIView):
    """
    TODO 나중에 형태가 갖춰지면, serializer를 추가하여 직렬화를 할 것.
    """
    
    def post(self, request: HttpRequest) -> HttpResponse:
        summary = ""
        keywords = []
        
        ## 원문 가져오기
        docs = request.POST.get("docs-input")
        
        if docs:
            ## 요약 및 키워드 추출
            summary = do_abssumm(docs)
            keywords = do_keywordext(docs)
        
        ## API 반환 데이터 생성
        data = {
            "summary": summary,
            "keywords": keywords,
        }
        
        return Response(data=data, status=201)