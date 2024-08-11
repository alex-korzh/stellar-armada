from dataclasses import dataclass
from typing import Callable


@dataclass
class MenuItem:
    title: str
    id: int
    callback: Callable
