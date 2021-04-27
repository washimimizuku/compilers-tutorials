from token_class import Token, TokenType

class Lexer():

    def __init__(self, code: str) -> None:
        self.code = code
        self.position = 0 # Current position in input (points to current char)
        self.read_position = 0 # Current reading position in input (after current char)
        self.ch = '' # Current char under examination

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

        if self.ch == '=':
            tok = Token(TokenType.ASSIGN, self.ch)
        elif self.ch == ';':
            tok = Token(TokenType.SEMICOLON, self.ch)
        elif self.ch == '(':
            tok = Token(TokenType.LPAREN, self.ch)
        elif self.ch == ')':
            tok = Token(TokenType.RPAREN, self.ch)
        elif self.ch == ',':
            tok = Token(TokenType.COMMA, self.ch)
        elif self.ch == '+':
            tok = Token(TokenType.PLUS, self.ch)
        elif self.ch == '{':
            tok = Token(TokenType.LBRACE, self.ch)
        elif self.ch == '}':
            tok = Token(TokenType.RBRACE, self.ch)
        elif self.ch == "\0":
            tok = Token(TokenType.EOF, "")

        self.read_char()

        return tok



import unittest

class TestLexer(unittest.TestCase):

    def test_lexer(self):
        code = '=+(){},;'
        lexer = Lexer(code)

        expected_results = [
            {
                "tp": "TokenType.ASSIGN",
                "literal": "="
            },
            {
                "tp": "TokenType.PLUS",
                "literal": "+"
            },
            {
                "tp": "TokenType.LPAREN",
                "literal": "("
            },
            {
                "tp": "TokenType.RPAREN",
                "literal": ")"
            },
            {
                "tp": "TokenType.LBRACE",
                "literal": "{"
            },
            {
                "tp": "TokenType.RBRACE",
                "literal": "}"
            },
            {
                "tp": "TokenType.COMMA",
                "literal": ","
            },
            {
                "tp": "TokenType.SEMICOLON",
                "literal": ";"
            },
            {
                "tp": "TokenType.EOF",
                "literal": ""
            }
        ]

        for i in range(len(code)):
            token = lexer.next_token()
            self.assertEqual(code[i], token.literal)
            self.assertEqual(expected_results[i]["tp"], str(token.tp))
            self.assertEqual(expected_results[i]["literal"], token.literal)


if __name__ == '__main__':
    unittest.main()