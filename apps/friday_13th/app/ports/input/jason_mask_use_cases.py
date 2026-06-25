from abc import ABC, abstractmethod


class JasonMaskUseCase(ABC):
    @abstractmethod
    def mask(self, username: str, password: str) -> bool:
        pass