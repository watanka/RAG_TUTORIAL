from langchain_core.documents import Document
from scheduled.src.crawl import TrafilaturaCrawler
from scheduled.src.jobs import repo, summarize, updater


crawler = TrafilaturaCrawler()
feed_url = "https://www.mk.co.kr/rss/50300009/"

contents = crawler.collect(feed_url)

print(summarize(contents[0]))

sample_summary_to_save = '''한국의 아파트 추첨 시장은 최근 증가 추세를 보이고 있으며, 특히 강남 지역을 중심으로 재건축 사업 등으로 뜨거운 경쟁이 이어지고 있습니다. 정부의 정책 변화와 함께 결혼한 부부나 다자녀 가정 등을 위한 특별 공급 정책도 수요 증가에 영향을 미치고 있습니다.  그러나 부동산 시장의 높은 수요와 치열한 경쟁은 주택 시장이 진정한 주택 구매자들을 위해 더 나은 방향으로 발전할 수 있도록 정부의 추가 개혁을 요구하고 있습니다.'''

doc = Document(page_content=sample_summary_to_save)
ids = ['20241007_서울_송파_가락_아파트_111']

# 내용 저장
# updater.update([doc], ids=ids)

# 내용 확인
print(repo.query_by_id(ids))

# 내용 필터링