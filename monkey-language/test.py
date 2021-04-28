from lexer import Lexer
import unittest

class TestLexer(unittest.TestCase):

    def test_lexer_basic(self):
        code = '=+(){},;'
        lexer = Lexer(code)

        expected = [
            ["TokenType.ASSIGN", "="],
            ["TokenType.PLUS", "+"],
            ["TokenType.LPAREN", "("],
            ["TokenType.RPAREN", ")"],
            ["TokenType.LBRACE", "{"],
            ["TokenType.RBRACE", "}"],
            ["TokenType.COMMA", ","],
            ["TokenType.SEMICOLON", ";"],
            ["TokenType.EOF", ""],
        ]

        for i in range(len(code)):
            token = lexer.next_token()
            self.assertEqual(code[i], token.literal)
            self.assertEqual(expected[i][0], str(token.token_type))
            self.assertEqual(expected[i][1], token.literal)

    def test_lexer_second(self):
        code = '''let five = 5;
let ten = 10;
   let add = fn(x, y) {
     x + y;
};
let result = add(five, ten);'''
        lexer = Lexer(code)

        expected = [
            ["TokenType.LET", "let"], 
            ["TokenType.IDENT", "five"], 
            ["TokenType.ASSIGN", "="], 
            ["TokenType.INT", "5"], 
            ["TokenType.SEMICOLON", ";"], 
            ["TokenType.LET", "let"], 
            ["TokenType.IDENT", "ten"], 
            ["TokenType.ASSIGN", "="], 
            ["TokenType.INT", "10"], 
            ["TokenType.SEMICOLON", ";"], 
            ["TokenType.LET", "let"], 
            ["TokenType.IDENT", "add"], 
            ["TokenType.ASSIGN", "="], 
            ["TokenType.FUNCTION", "fn"], 
            ["TokenType.LPAREN", "("], 
            ["TokenType.IDENT", "x"],
            ["TokenType.COMMA", ","], 
            ["TokenType.IDENT", "y"], 
            ["TokenType.RPAREN", ")"],
            ["TokenType.LBRACE", "{"],
            ["TokenType.IDENT", "x"],
            ["TokenType.PLUS", "+"],
            ["TokenType.IDENT", "y"],
            ["TokenType.SEMICOLON", ";"],
            ["TokenType.RBRACE", "}"],
            ["TokenType.SEMICOLON", ";"],
            ["TokenType.LET", "let"],
            ["TokenType.IDENT", "result"],
            ["TokenType.ASSIGN", "="],
            ["TokenType.IDENT", "add"],
            ["TokenType.LPAREN", "("],
            ["TokenType.IDENT", "five"],
            ["TokenType.COMMA", ","],
            ["TokenType.IDENT", "ten"],
            ["TokenType.RPAREN", ")"],
            ["TokenType.SEMICOLON", ";"],
            ["TokenType.EOF", ""],
        ]

        for i in range(len(code)):
            token = lexer.next_token()
            self.assertEqual(code[i], token.literal)
            self.assertEqual(expected[i][0], str(token.token_type))
            self.assertEqual(expected[i][1], token.literal)


if __name__ == '__main__':
    unittest.main()