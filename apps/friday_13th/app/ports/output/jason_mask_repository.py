from abc import ABC, abstractmethod


class JasonMaskRepository(ABC):
    @abstractmethod
    def mask(self, username: str, password: str) -> bool:
        pass