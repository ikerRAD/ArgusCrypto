from dataclasses import dataclass


@dataclass(frozen=True)
class Exchange:
    id: int
    name: str
