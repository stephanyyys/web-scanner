from abc import ABC, abstractmethod

class ScannerModule(ABC):
    @abstractmethod
    def run(self, url: str):
        pass