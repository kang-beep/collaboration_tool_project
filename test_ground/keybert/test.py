"""
## 개요
해당 파일은 KeyBert + 한국어 전용 sentence transformer를 결합하여
핵심 키워드를 추출하는 예시입니다.

## 유의사항
- stopwords.txt 에서 불용어를 사용. 불용어 추가를 원하면 해당 파일에 추가
- 핵심 키워드는 최대 5개 이며, 무조건 5개가 나오지 않음. 예시코드 사용시 이를 고려할 것.

"""

import re

from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT



## 원문
docs = """
와, 샌즈! 언더테일 아시는구나! 혹시 모르시는분들에 대해[1] 설명해드립니다 샌즈랑[2] 언더테일의 세가지 엔딩루트중 몰살엔딩의 최종보스로 진.짜.겁.나.어.렵.습.니.다 공격은 전부다 회피하고 만피가 92인데 샌즈의 공격은 1초당 60이 다는데다가[3] 독뎀까지 추가로 붙어있습니다.. 하지만 이러면 절대로 게임을 깰 수 가없으니 제작진이 치명적인 약점을 만들었죠. 샌즈의 치명적인 약점이 바로 지친다는것입니다. 패턴들을 다 견디고나면 지쳐서 자신의 턴을 유지한채로 잠에듭니다. 하지만 잠이들었을때 창을옮겨서 공격을 시도하고 샌즈는 1차공격은 피하지만 그 후에 바로날아오는 2차 공격을 맞고 죽습니다.
"""

## 모델 불러오기
st_model = SentenceTransformer("jhgan/ko-sroberta-multitask")
kw_model = KeyBERT(model=st_model)

## 불용어 불러오기
stopwords_path = "/home/kangsan/collaboration_tool_project/test_ground/keybert/stopwords.txt"
stopwords = set()
with open(stopwords_path, "r", encoding="UTF-8") as file:
    for line in file:
        stopword = line.strip()
        stopwords.add(stopword)

## 추론 - 불용어가 포함된 keyword 추출.
# ex) [("키워드1", 중요도_실수값1), ("키워드2", 중요도_실수값2), ...]
keywords = kw_model.extract_keywords(docs=docs, highlight=True)

processed_keywords = set()
stopwords_pattern = "|".join([word + "$" for word in stopwords])  # ex) 는$|를$|이$|...
for keyword in keywords:
    processed_keyword = re.sub(stopwords_pattern, "", keyword[0])
    processed_keywords.add(processed_keyword)

print("전체 키워드: ", *processed_keywords)
