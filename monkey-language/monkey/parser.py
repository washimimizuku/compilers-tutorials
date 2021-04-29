from monkey.ast import Program
from monkey.lexer import Lexer
from monkey.token import Token


class Parser():
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = None
        self.peek_token = None

        # Read two tokens, so current_token and peek_token are both set
        self.next_token()
        self.next_token()

    def next_token(self) -> None:
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self) -> Program:
        return None
