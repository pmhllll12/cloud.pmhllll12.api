from abc import ABC, abstractmethod

class PamelaCookUseCase(ABC):
    @abstractmethod
    def signup(self, username: str, password: str) -> bool:
        pass
        