from abc import ABC, abstractmethod


class Response:
    pass


class Instruction(ABC):
    @abstractmethod
    def execute(self, *args) -> Response | None:
        pass
