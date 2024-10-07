from abc import ABC, abstractmethod

class DataHandler(ABC):
    @abstractmethod
    def __execute__(self):
        raise NotImplementedError
    

class ChromaDataHandler(DataHandler):


    def __execute__(self):
        pass