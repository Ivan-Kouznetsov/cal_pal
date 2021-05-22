from typing import List, Union

from .node import Node
from .token import Token, TokenType


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = iter(tokens)
        self.advance_to_next_token()

    def advance_to_next_token(self) -> None:
        self.current_token = next(self.tokens, None)

    def parse(self) -> Node:
        result = self.next_expr()

        if self.current_token is not None:
            raise Exception("parse: Invalid syntax")

        return result

    # looks for expressions (i.e. operations with lowest precedence)
    def next_expr(self) -> Node:
        result = self.next_factor()

        while self.current_token is not None and self.current_token.type in (
            TokenType.Add,
            TokenType.Subtract,
        ):
            this_token = self.current_token
            self.advance_to_next_token()

            result = Node(this_token.type, result, self.next_factor())

        return result

    # looks for factors (i.e. operations with highest precedence)
    def next_factor(self) -> Node:
        result = self.next_term()

        while self.current_token is not None and self.current_token.type in (
            TokenType.Multiply,
            TokenType.Divide,
        ):
            this_token = self.current_token
            self.advance_to_next_token()

            result = Node(this_token.type, result, self.next_term())

        return result

    # looks for terms (i.e. values)
    def next_term(self) -> Node:
        this_token = self.current_token

        if this_token is not None:

            if this_token.type == TokenType.OpeningBracket:
                self.advance_to_next_token()
                result = self.next_expr()

                if (
                    self.current_token is None
                    or self.current_token.type != TokenType.ClosingBracket
                ):
                    raise Exception("next_term: Invalid syntax")

                self.advance_to_next_token()
                return result

            if this_token.type == TokenType.Number:
                self.advance_to_next_token()
                return Node(TokenType.Number, this_token.value)

        raise Exception("next_term: Expected a token")
