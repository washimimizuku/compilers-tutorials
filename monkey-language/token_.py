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

    def __init__(self, token_type: TokenType, literal: str) -> None:
        self.token_type = token_type
        self.literal = literal
