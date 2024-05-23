## 문서요약 테스트

### 프론트엔드
#### 입력 페이지
- [x] 입력 페이지 구현

#### 결과 페이지
- [x] (처리성능 향상 목적) AJAX를 통해 결과 인공지능 추론결과 요청 보내기.
- [ ] 텍스트 문단별로 분류 목차
- [ ] 문단별로 요약 표기창
- [ ] 핵심 단어 밑줄 반환

### 백엔드
#### Django General
- [ ] 텍스트 INPUT DB에 저장
- [x] 텍스트 INPUT 문단/전체 SUMM 진행
- [ ] 텍스트 INPUT에 대한 하이라이트(중요한 문장 또는 키워드) 표기

#### Django REST framework
- [x] (처리성능 향상 목적) Pytorch 토크나이저 및 모델을 불러오는 LazyLoader 싱글톤 클래스 구현
- [x] (처리성능 향상 목적) 비동기 API를 구현하여 모델 추론 결과 받아보기 
- [ ] (docsumm/api/docsumm_api.py) serializers 추가 


