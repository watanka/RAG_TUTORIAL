import pytest
from scheduled.src.crawl import TrafilaturaCrawler


crawler = TrafilaturaCrawler()

URL = "https://www.mk.co.kr/rss/50300009/"

def test_크롤링이_실패없이_동작한다():
    contents = crawler.collect(URL)
    assert type(contents) == list
    
def test_크롤한_정보들을_요약한다():
    contents = crawler.collect(URL)
    