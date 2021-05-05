from monkey.ast import Program, LetStatement, Identifier
from monkey.token import Token, TokenType
import unittest


class TestAST(unittest.TestCase):

    def test_string(self):
        program = Program()

        statement = LetStatement(Token(TokenType.LET, "let"))
        statement.name = Identifier(Token(TokenType.IDENT, "myVar"), "myVar")
        statement.value = Identifier(
            Token(TokenType.IDENT, "anotherVar"), "anotherVar")

        program.statements.append(statement)

        self.assertEqual(str(program), "let myVar = anotherVar;",
                         f"String representation for program is wrong, got {str(program)}")
