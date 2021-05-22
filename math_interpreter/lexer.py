import re
from typing import Final

from .token import Token, TokenType


class Lexer:
    def __init__(self, text: str):
        self.text = iter(text)
        self.next_char()

    @staticmethod
    def _is_match(pattern: str, text: str) -> bool:
        match = re.match(pattern, text)
        if match is None:
            return False

        return match[0] == text

    def _is_at_num_char(self) -> bool:
        return (
            Lexer._is_match(r"[0-9]|\.", self.current_char)
            if self.current_char is not None
            else False
        )

    def _is_at_whitespace_char(self) -> bool:
        return (
            Lexer._is_match(r"\n|\t|\s", self.current_char)
            if self.current_char is not None
            else False
        )

    def next_char(self) -> None:
        self.current_char = next(self.text, None)

    def generate_tokens(self):
        while self.current_char is not None:
            if self._is_at_whitespace_char():
                self.next_char()
            elif self._is_at_num_char():
                yield self.generate_number()
            elif self.current_char == "+":
                self.next_char()
                yield Token(TokenType.Add)
            elif self.current_char == "-":
                self.next_char()
                yield Token(TokenType.Subtract)
            elif self.current_char == "*":
                self.next_char()
                yield Token(TokenType.Multiply)
            elif self.current_char == "/":
                self.next_char()
                yield Token(TokenType.Divide)
            elif self.current_char == "(":
                self.next_char()
                yield Token(TokenType.OpeningBracket)
            elif self.current_char == ")":
                self.next_char()
                yield Token(TokenType.ClosingBracket)
            else:
                raise Exception(f"Illegal character '{self.current_char}'")

    def generate_number(self) -> Token:
        dot: Final[str] = "."
        dot_count = 0
        number_str: str = self.current_char or ""
        self.next_char()

        while self.current_char is not None and self._is_at_num_char():
            if self.current_char == ".":
                dot_count += 1
                if dot_count > 1:
                    break

            number_str += self.current_char
            self.next_char()

        if number_str.startswith(dot):
            number_str = "0" + number_str
        if number_str.endswith(dot):
            number_str = number_str + "0"

        return Token(TokenType.Number, number_str)
