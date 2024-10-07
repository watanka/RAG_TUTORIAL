RAG 구조
![](rag_diagram.png)

진행방향
1. Data Collection <-
    - naver 뉴스 api에서 실시간 top 10위 뉴스를 긁어오자.
2. Data Embedding
3. Vector DB 구성 (Retrieval, Indexing)
4. LLM 설정
5. Prompt 설정
6. Chain 설정
7. UI 설정. 고려할 요소 Streaming, ChatHistory

Prompt




- [ ] : https 붙이기

크롤링 -> preprocess -> 벡터 DB에 저장

preprocess: 길이가 길어질 경우, 잘라서 요약
preprocess 부분: 어떤 식으로 저장되는 게 좋을까?

요약 저장 시에, 날짜와 관련 지역, 키워드 등으로 정리