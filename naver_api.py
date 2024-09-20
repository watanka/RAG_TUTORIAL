import requests
from langchain.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup

client_id = "CJoKN_xbapDDgycfdWaM"
client_secret = "QTyXdZ2d7c"
url = "https://openapi.naver.com/v1/search/news.json" 
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과


# 뉴스 본문 추출 함수
def get_news_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 다양한 태그에서 본문 추출
        content = None
        possible_selectors = [
            "article",              # <article> 태그
            ".article",             # 특정 클래스
            ".news_body",           # 일반적인 뉴스 본문 클래스
            ".post-content",        # 블로그 스타일
            ".entry-content",       # 워드프레스 스타일
            ".content",             # 일반적인 내용 클래스
            "#content",             # ID로 찾기
            "#articleBody",         # Naver 등에서 사용
            "#dic_area"            # Naver 뉴스 본문
        ]
        
        for selector in possible_selectors:
            element = soup.select_one(selector)
            if element:
                content = element.get_text(strip=True)
                break
        
        if content:
            return content
        else:
            return "본문 추출 실패: 해당 선택자에서 콘텐츠를 찾을 수 없습니다."
    
    except Exception as e:
        return f"Error fetching content: {e}"


params = {
    'query': "부동산",
    'display': 10,
    'sort': 'date'
}

headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}

response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    for idx, item in enumerate(data['items'], 1):
        print(f"{idx}. Title: {item['title']}")
        print(f"   Link: {item['link']}")
        # loader = WebBaseLoader(item['link'])
        # documents = loader.load()
        documents = get_news_content(item['link'])

        print(documents)
else:
    print(f"Error {response.status_code}: Unable to fetch news")
