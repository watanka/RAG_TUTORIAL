from abc import ABC, abstractmethod

from trafilatura import feeds, fetch_url, extract


class Crawler(ABC):
    @abstractmethod
    def collect(self, url):
        raise NotImplementedError


class TrafilaturaCrawler(Crawler):

    def collect(self, url) -> list[str]:
        contents = []
        feed_list = feeds.find_feed_urls(url)
        
        for feed in feed_list:
            html = fetch_url(feed)
            text = extract(html)
            contents.append(text)
    
        return contents


