from lexer import Lexer
from token_ import TokenType
import unittest


class TestLexer(unittest.TestCase):

    def test_lexer_basic(self):
        code = '=+(){},;'
        lexer = Lexer(code)

        expected = [
            [TokenType.ASSIGN.name, "="],
            [TokenType.PLUS.name, "+"],
            [TokenType.LPAREN.name, "("],
            [TokenType.RPAREN.name, ")"],
            [TokenType.LBRACE.name, "{"],
            [TokenType.RBRACE.name, "}"],
            [TokenType.COMMA.name, ","],
            [TokenType.SEMICOLON.name, ";"],
            [TokenType.EOF.name, ""],
        ]

        for i in range(len(code)):
            token = lexer.next_token()
            self.assertEqual(code[i], token.literal)
            self.assertEqual(expected[i][0], token.token_type.name)
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
            [TokenType.LET.name, "let"], 
            [TokenType.IDENT.name, "five"], 
            [TokenType.ASSIGN.name, "="], 
            [TokenType.INT.name, "5"], 
            [TokenType.SEMICOLON.name, ";"], 
            [TokenType.LET.name, "let"], 
            [TokenType.IDENT.name, "ten"], 
            [TokenType.ASSIGN.name, "="], 
            [TokenType.INT.name, "10"], 
            [TokenType.SEMICOLON.name, ";"], 
            [TokenType.LET.name, "let"], 
            [TokenType.IDENT.name, "add"], 
            [TokenType.ASSIGN.name, "="], 
            [TokenType.FUNCTION.name, "fn"], 
            [TokenType.LPAREN.name, "("], 
            [TokenType.IDENT.name, "x"],
            [TokenType.COMMA.name, ","], 
            [TokenType.IDENT.name, "y"], 
            [TokenType.RPAREN.name, ")"],
            [TokenType.LBRACE.name, "{"],
            [TokenType.IDENT.name, "x"],
            [TokenType.PLUS.name, "+"],
            [TokenType.IDENT.name, "y"],
            [TokenType.SEMICOLON.name, ";"],
            [TokenType.RBRACE.name, "}"],
            [TokenType.SEMICOLON.name, ";"],
            [TokenType.LET.name, "let"],
            [TokenType.IDENT.name, "result"],
            [TokenType.ASSIGN.name, "="],
            [TokenType.IDENT.name, "add"],
            [TokenType.LPAREN.name, "("],
            [TokenType.IDENT.name, "five"],
            [TokenType.COMMA.name, ","],
            [TokenType.IDENT.name, "ten"],
            [TokenType.RPAREN.name, ")"],
            [TokenType.SEMICOLON.name, ";"],
            [TokenType.EOF.name, ""],
        ]

        for i in range(len(code)):
            token = lexer.next_token()
            self.assertEqual(code[i], token.literal)
            self.assertEqual(expected[i][0], token.token_type.name)
            self.assertEqual(expected[i][1], token.literal)


if __name__ == '__main__':
    unittest.main()