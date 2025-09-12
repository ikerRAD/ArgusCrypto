from abc import ABC, abstractmethod


class RouteHandler(ABC):
    @abstractmethod
    def handle(self) -> dict:
        pass
