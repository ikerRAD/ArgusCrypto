from abc import ABC, abstractmethod

from pydantic import BaseModel


class RouteHandler(ABC):
    @abstractmethod
    def handle(self) -> BaseModel | list[BaseModel]:
        pass
