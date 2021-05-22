from typing import Optional

from .lexer import Lexer
from .math_parser import Parser
from .node import Node
from .token import TokenType


def _calc(node: Node):
    if node.type == TokenType.Number:
        assert isinstance(node.left, str)
        return float(node.left)

    assert isinstance(node.left, Node)
    assert isinstance(node.right, Node)

    if node.type == TokenType.Add:
        return _calc(node.left) + _calc(node.right)
    if node.type == TokenType.Subtract:
        return _calc(node.left) - _calc(node.right)
    if node.type == TokenType.Divide:
        return _calc(node.left) / _calc(node.right)
    if node.type == TokenType.Multiply:
        return _calc(node.left) * _calc(node.right)


def calc(math_expr: str) -> float:
    lexer = Lexer(math_expr)
    tokens = lexer.generate_tokens()
    parser = Parser(tokens)
    tree = parser.parse()

    return _calc(tree)
