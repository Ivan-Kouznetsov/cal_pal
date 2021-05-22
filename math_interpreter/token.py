from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    Number = auto()
    Add = auto()
    Subtract = auto()
    Multiply = auto()
    Divide = auto()
    OpeningBracket = auto()
    ClosingBracket = auto()


@dataclass
class Token:
    type: TokenType
    value: Any = None
