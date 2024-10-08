from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def add(self):
        raise NotImplementedError
    

class ChromaRepository(Repository):
    def __init__(self, db):
        self.db = db
    
    def add(self, contents, ids):
        self.db.add_documents(documents = contents, ids=ids)

    def query_by_id(self, ids):
        return self.db.get(ids=ids)
