from abc import ABC, abstractmethod

# Vector DB에 하루에 한번씩 업데이트
# db: 저장할 데이터베이스.
# data_handler: 정보를 데이터베이스에 저장하기 위해 필요한 처리를 담당하는 클래스


class DailyUpdater(ABC):
    @abstractmethod
    def update(self, contents):
        raise NotImplementedError



class ChromaDailyUpdater(DailyUpdater):

    def __init__(self, repository):
        self.repository = repository

    def update(self, contents, ids):
        self.repository.add(contents, ids = ids)
