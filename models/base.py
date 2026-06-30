from abc import ABC, abstractmethod

class EntidadeBase(ABC):
    @abstractmethod
    def para_dict(self) -> dict:
        pass

    @abstractmethod
    def validar(self) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
