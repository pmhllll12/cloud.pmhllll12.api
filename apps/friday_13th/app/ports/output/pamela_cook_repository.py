from abc import ABC, abstractmethod

class PamelaCookRepository(ABC):
    @abstractmethod
    def signup(self, username: str, password: str) -> bool:
        pass
        