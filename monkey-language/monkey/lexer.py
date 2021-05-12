from monkey.token import Token, TokenType


class Lexer():
    def __init__(self, code: str) -> None:
        self.code = code
        self.position = 0  # Current position in input (points to current char)
        # Current reading position in input (after current char)
        self.read_position = 0
        self.ch = ''  # Current char under examination

        self.read_char()

    def read_char(self) -> None:
        if self.read_position >= len(self.code):
            self.ch = '\0'
        else:
            self.ch = self.code[self.read_position]

        self.position = self.read_position
        self.read_position += 1

    def next_token(self) -> Token:
        tok: Token

        self.skip_whitespace()

        if self.ch == '=':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                literal = ch + self.ch
                tok = Token(TokenType.EQ, literal)
            else:
                tok = Token(TokenType.ASSIGN, self.ch)
        elif self.ch == '+':
            tok = Token(TokenType.PLUS, self.ch)
        elif self.ch == '-':
            tok = Token(TokenType.MINUS, self.ch)
        elif self.ch == '!':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                literal = ch + self.ch
                tok = Token(TokenType.NOT_EQ, literal)
            else:
                tok = Token(TokenType.BANG, self.ch)
        elif self.ch == '/':
            tok = Token(TokenType.SLASH, self.ch)
        elif self.ch == '*':
            tok = Token(TokenType.ASTERISK, self.ch)
        elif self.ch == '<':
            tok = Token(TokenType.LT, self.ch)
        elif self.ch == '>':
            tok = Token(TokenType.GT, self.ch)
        elif self.ch == ';':
            tok = Token(TokenType.SEMICOLON, self.ch)
        elif self.ch == ',':
            tok = Token(TokenType.COMMA, self.ch)
        elif self.ch == '(':
            tok = Token(TokenType.LPAREN, self.ch)
        elif self.ch == ')':
            tok = Token(TokenType.RPAREN, self.ch)
        elif self.ch == '{':
            tok = Token(TokenType.LBRACE, self.ch)
        elif self.ch == '}':
            tok = Token(TokenType.RBRACE, self.ch)
        elif self.ch == '[':
            tok = Token(TokenType.LBRACKET, self.ch)
        elif self.ch == ']':
            tok = Token(TokenType.RBRACKET, self.ch)
        elif self.ch == "\0":
            tok = Token(TokenType.EOF, "")
        elif self.ch == '"':
            tok = Token(TokenType.STRING, self.read_string())
        else:
            if self.is_letter(self.ch):
                literal = self.read_identifer()
                token_type = self.lookup_identifier(literal)
                tok = Token(token_type, literal)
                return tok
            elif self.is_digit(self.ch):
                tok = Token(TokenType.INT, self.read_number())
                return tok
            else:
                tok = Token(TokenType.ILLEGAL, self.ch)

        self.read_char()

        return tok

    def read_identifer(self) -> str:
        position = self.position

        while self.is_letter(self.ch):
            self.read_char()

        return self.code[position:self.position]

    def is_letter(self, ch: str) -> bool:
        return ch.isalpha() or ch == '_'

    def read_number(self) -> str:
        position = self.position

        while self.is_digit(self.ch):
            self.read_char()

        return self.code[position:self.position]

    def is_digit(self, ch: str) -> bool:
        return ch.isdigit()

    def lookup_identifier(self, identifier: str) -> TokenType:
        if identifier in Token.KEYWORDS.keys():
            return Token.KEYWORDS[identifier]
        else:
            return TokenType.IDENT

    def skip_whitespace(self):
        while self.ch in [' ', '\t', '\r', '\n']:
            self.read_char()

    def peek_char(self):
        if self.read_position >= len(self.code):
            return 0
        else:
            return self.code[self.read_position]

    def read_string(self) -> str:
        position = self.position + 1

        self.read_char()
        while self.ch not in ['"', 0]:
            self.read_char()

        return self.code[position:self.position]
