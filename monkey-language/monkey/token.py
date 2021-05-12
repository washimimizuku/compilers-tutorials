import enum


class TokenType(enum.Enum):
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers and literals
    IDENT = "IDENT"  # add, foobar, x, y, ...
    INT = "INT"  # 1343456
    STRING = "STRING"

    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"

    LT = "<"
    GT = ">"
    EQ = "=="
    NOT_EQ = "!="

    # Delimeters
    COMMA = ","
    SEMICOLON = ";"

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"

    # Keywords
    FUNCTION = "FUNCTION"
    LET = "LET"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"


class Token:
    KEYWORDS = {
        'fn': TokenType.FUNCTION,
        'let': TokenType.LET,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'return': TokenType.RETURN,
    }

    def __init__(self, token_type: TokenType, literal: str) -> None:
        self.token_type = token_type
        self.literal = literal

    def __str__(self) -> str:
        tok = {'token_type': self.token_type.name, 'literal': self.literal}
        return str(tok)
