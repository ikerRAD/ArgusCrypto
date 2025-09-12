from abc import ABC, abstractmethod


class TaskHandler(ABC):
    @abstractmethod
    def handle(self) -> None:
        pass
