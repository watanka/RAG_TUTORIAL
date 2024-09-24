from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def add(self):
        raise NotImplementedError
    

class ChromaRepository(Repository):
    def __init__(self, db):
        self.db = db
    
    def add(self, contents):
        self.db.add_documents(documents = contents)
