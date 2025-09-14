from abc import ABC, abstractmethod

from pydantic import BaseModel


class RouteHandler(ABC):
    @abstractmethod
    def handle(self, *args) -> BaseModel | list[BaseModel]:
        pass
