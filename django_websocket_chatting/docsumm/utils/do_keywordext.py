import re
from docsumm.utils.lazy_loader import LazyLoader


def do_keywordext(docs: str) -> list:
    ## 모델 불러오기
    lazy_loader = LazyLoader()
    kw_model = lazy_loader.get_keybert_model()

    ## 불용어 불러오기
    stopwords_path = "/home/kangsan/collaboration_tool_project/django_websocket_chatting/docsumm/utils/stopwords.txt"
    stopwords = set()
    with open(stopwords_path, "r", encoding="UTF-8") as file:
        for line in file:
            stopword = line.strip()
            stopwords.add(stopword)

    ## 추론 - 불용어가 포함된 keyword 추출.
    # ex) [("키워드1", 중요도_실수값1), ("키워드2", 중요도_실수값2), ...]
    keywords = kw_model.extract_keywords(docs=docs)
    
    # 후처리 - 불용어 제거
    processed_keywords = set()
    stopwords_pattern = "|".join([word + "$" for word in stopwords])  # ex) 는$|를$|이$|...
    for keyword in keywords:
        processed_keyword = re.sub(stopwords_pattern, "", keyword[0])
        processed_keywords.add(processed_keyword)
        
    return processed_keywords