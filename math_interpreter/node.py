from dataclasses import dataclass
from typing import Union

from .token import TokenType


@dataclass
class Node:
    type: TokenType
    left: Union[None, str, "Node"] = None
    right: Union[None, str, "Node"] = None

    def __repr__(self):
        if self.type == TokenType.Number:
            return self.left
        if self.type == TokenType.Add:
            return f"{self.left}+{self.right}"
        if self.type == TokenType.Subtract:
            return f"{self.left}-{self.right}"
        if self.type == TokenType.Multiply:
            return f"{self.left}*{self.right}"
        if self.type == TokenType.Divide:
            return f"{self.left}/{self.right}"
