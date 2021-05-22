from math_interpreter.node import Node
from math_interpreter.token import TokenType


def test_repr():
    assert str(Node(TokenType.Add, "1", "2")) == "1+2"
    assert str(Node(TokenType.Subtract, "1", "2")) == "1-2"
    assert str(Node(TokenType.Multiply, "1", "2")) == "1*2"
    assert str(Node(TokenType.Divide, "1", "2")) == "1/2"
    assert str(Node(TokenType.Number, "1", "2")) == "1"
