import numpy as np
from pytesseract import Output
import pytesseract
import cv2


## opencv 이미지 불러오기.
file_name = "ocr_test.jpg"
img = cv2.imread(file_name)
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # (선택) 흑백으로 변환
denoised_img = cv2.medianBlur(gray_image, 5)  # (선택) 중간값 블러를 사용하여 잡음 제거

result1 = pytesseract.image_to_string(image=denoised_img, lang="kor")
result2 = pytesseract.image_to_string(image=denoised_img, lang="eng")
result3 = pytesseract.image_to_string(image=denoised_img, lang="kor+eng")


## 주의! 한글 결과 출력을 원하면 한글 데이터셋 파일이 있어야 할것.
print(result1)  # 한글만 결과
print(result2)  # 영어만 결과
print(result3)  # 한글+영어 결과


"""
유의! 언어 설정 시, 해당 언어가 없으면
가장 비슷한 단어를 억지로 결과값으로 내놓는다.


# 출력 결과

## result1
핸드 드라이어
(500 6401091)

##  result2
— @c CPO)
(Son Gunjogi)

ㄴ- 핸드 드라이어
(Son Gunjogi)

"""