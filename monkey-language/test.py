from lexer import Lexer
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