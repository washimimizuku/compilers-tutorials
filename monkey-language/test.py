from lexer import Lexer
from token_ import TokenType
import unittest


class TestLexer(unittest.TestCase):

    def test_basic_operators(self):
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

        for i in range(len(expected)):
            token = lexer.next_token()
            self.assertEqual(expected[i][0], token.token_type.name)
            self.assertEqual(expected[i][1], token.literal)

    def test_variables_and_functions(self):
        code = '''let five = 5;
let ten = 10;
   let add = fn(x, y) {
     x + y;
};
let result = add(five, ten);
'''
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

        for i in range(len(expected)):
            token = lexer.next_token()
            self.assertEqual(expected[i][0], token.token_type.name)
            self.assertEqual(expected[i][1], token.literal)

    def test_advanced_operators(self):
        code = "!-/*5;"
        lexer = Lexer(code)

        expected = [
            [TokenType.BANG.name, "!"],
            [TokenType.MINUS.name, "-"],
            [TokenType.SLASH.name, "/"],
            [TokenType.ASTERISK.name, "*"],
            [TokenType.INT.name, "5"],
            [TokenType.SEMICOLON.name, ";"],
            [TokenType.EOF.name, ""],
        ]

        for i in range(len(expected)):
            token = lexer.next_token()
            self.assertEqual(expected[i][0], token.token_type.name)
            self.assertEqual(expected[i][1], token.literal)

    def test_if_else(self):
        code = '''if (5 < 10) {
    return true;
} else {
    return false;
}
'''
        lexer = Lexer(code)

        expected = [
            [TokenType.IF.name, "if"],
            [TokenType.LPAREN.name, "("],
            [TokenType.INT.name, "5"],
            [TokenType.LT.name, "<"],
            [TokenType.INT.name, "10"],
            [TokenType.RPAREN.name, ")"],
            [TokenType.LBRACE.name, "{"],
            [TokenType.RETURN.name, "return"],
            [TokenType.TRUE.name, "true"],
            [TokenType.SEMICOLON.name, ";"],
            [TokenType.RBRACE.name, "}"],
            [TokenType.ELSE.name, "else"],
            [TokenType.LBRACE.name, "{"],
            [TokenType.RETURN.name, "return"],
            [TokenType.FALSE.name, "false"],
            [TokenType.SEMICOLON.name, ";"],
            [TokenType.RBRACE.name, "}"],
            [TokenType.EOF.name, ""],
        ]

        for i in range(len(expected)):
            token = lexer.next_token()
            self.assertEqual(expected[i][0], token.token_type.name)
            self.assertEqual(expected[i][1], token.literal)

    def test_comparison_operators(self):
        code = '''5 < 10 > 5;
10 == 10;
10 != 9;
'''
        lexer = Lexer(code)

        expected = [
            [TokenType.INT.name, "5"],
            [TokenType.LT.name, "<"],
            [TokenType.INT.name, "10"],
            [TokenType.GT.name, ">"],
            [TokenType.INT.name, "5"],
            [TokenType.SEMICOLON.name, ";"],
            [TokenType.INT.name, "10"],
            [TokenType.EQ.name, "=="],
            [TokenType.INT.name, "10"],
            [TokenType.SEMICOLON.name, ";"],
            [TokenType.INT.name, "10"],
            [TokenType.NOT_EQ.name, "!="],
            [TokenType.INT.name, "9"],
            [TokenType.SEMICOLON.name, ";"],
            [TokenType.EOF.name, ""],
        ]

        for i in range(len(expected)):
            token = lexer.next_token()
            self.assertEqual(expected[i][0], token.token_type.name)
            self.assertEqual(expected[i][1], token.literal)



if __name__ == '__main__':
    unittest.main()
