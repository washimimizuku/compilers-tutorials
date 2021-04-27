import enum

class TokenType(enum.Enum):
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers and literals
    IDENT = "IDENT" # add, foobar, x, y, ...
    INT = "INT" # 1343456

    # Operators
    ASSIGN = "="
    PLUS = "+"

    # Delimeters
    COMMA = ","
    SEMICOLON = ";"

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Keywords
    FUNCTION = "FUNCTION"
    LET = "LET"


class Token:
    """Represents a token."""

    def __init__(self, tp: TokenType, literal: str) -> None:
        self.tp = tp
        self.literal = literal

    def __repr__(self) -> str:
        return f"<Token type: {self.tp} literal: {self.literal}>"

    def __str__(self) -> str:
        return f"<Token type: {self.tp} literal: {self.literal}>"
