## Requirements

```
pip install -r requirements.txt
```


## Usage

```
main.py / main2.py 실행하기

main.py => 해당 이미지의 OCR 결과값만 출력
main2.py => 해당 이미지의 OCR 인식 좌표값과 인식한 부분 이미지, 결과값까지 모두 제공
```

```
이미지 경로값 입력: (OCR 시킬 이미지 경로값 입력)

* 큰 따옴표나 작은 따옴표 사용 X
ex) C:\Users\image.JPG 와 같이 입력
```

## Update, 05/26
```
기존 이미지 형식의 확장자 파일만 OCR 할 수 있었던 상태에서
'.pdf', '.docx' 파일도 인식하여 OCR 할 수 있도록 기능 업데이트

.pdf 확장자는 pdf2image 라이브러리를 사용하였고,
.docx 확장자는 docx 라이브러리에서 OCR 모델을 사용해 인식하지 않아도 알아서 텍스트를 정확히 긁어와주는 기능을 갖추고 있었음.

* docx 라이브러리는 문서 형식 그대로 가져오기 때문에 엔터도 인식한 결과값을 출력함
OCR 모델을 사용하려면 docx2pdf 라이브러리로 pdf 변환 후 pdf2image를 사용해서 2중 구조를 사용해야함
```

