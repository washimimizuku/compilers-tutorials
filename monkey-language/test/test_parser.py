from monkey.ast import (
    Statement, LetStatement, ReturnStatement, ExpressionStatement,
    Identifier,
    IntegerLiteral,
    PrefixExpression
)
from monkey.lexer import Lexer
from monkey.parser import Parser
import unittest


class TestParser(unittest.TestCase):

    def test_let_statements(self):
        code = '''
let x = 5;
let y = 10;
let foobar = 838383;
'''
        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertNotEqual(program, None, "parse_program() returned None")
        self.assertEqual(len(program.statements), 3,
                         f"program.statements does not contain 3 statements. got={len(program.statements)}")

        expected = ['x', 'y', 'foobar']
        for i in range(len(program.statements)):
            self._test_let_statement(program.statements[i], expected[i])

    def test_invalid_let_statements(self):
        code = '''
let x 5;
let = 10;
let 838383;
'''
        lexer = Lexer(code)
        parser = Parser(lexer)

        parser.parse_program()
        with self.assertRaises(AssertionError):
            self._check_parser_errors(parser)

    def test_return_statements(self):
        code = '''
return 5;
return 10;
return 993322;
'''
        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 3,
                         f"program.statements does not contain 3 statements. got={len(program.statements)}")

        for statement in program.statements:
            self.assertIsInstance(statement, ReturnStatement,
                                  f"statement not 'return'. got={statement}")
            self.assertEqual(statement.token_literal(),
                             'return', f"statement.token_literal not 'return'. got={statement.token_literal()}")

    def test_identifier_expression(self):
        code = "foobar;"
        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        identifier = program.statements[0].expression
        self.assertIsInstance(identifier, Identifier,
                              f"expression is not an instance of Identifier. got={type(identifier)}")
        self.assertEqual(identifier.value, "foobar",
                         f"identifier.value not foobar. got={identifier.value}")
        self.assertEqual(identifier.token_literal(), "foobar",
                         f"identifier.token_literal() not foobar. got={identifier.token_literal()}")

    def test_integer_literal_expression(self):
        code = "5;"
        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        literal = program.statements[0].expression
        self.assertIsInstance(literal, IntegerLiteral,
                              f"expression is not an instance of IntegerLiteral. got={type(literal)}")
        self.assertEqual(literal.value, 5,
                         f"literal.value not 5. got={literal.value}")
        self.assertEqual(literal.token_literal(), "5",
                         f"literal.token_literal() not 5. got={literal.token_literal()}")

    def test_parsing_prefix_expressions(self):
        prefix_tests = [
            ["!5", "!", 5],
            ["-15", "-", 15]
        ]

        for test in prefix_tests:
            code = test[0]
            lexer = Lexer(code)
            parser = Parser(lexer)

            program = parser.parse_program()
            self._check_parser_errors(parser)

            self.assertEqual(len(program.statements), 1,
                             f"program.statements does not contain 1 statement. got={len(program.statements)}")
            self.assertIsInstance(program.statements[0], ExpressionStatement,
                                  f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

            expression = program.statements[0].expression
            self.assertIsInstance(expression, PrefixExpression,
                                  f"expression is not an instance of PrefixExpression. got={type(expression)}")
            self.assertEqual(expression.operator, test[1],
                             f"expression.value not {test[1]}. got={expression.operator}")
            self._test_integer_literal(expression.right, test[2])

    def _test_let_statement(self, statement: Statement, name: str):
        self.assertEqual(statement.token_literal(),
                         'let', f"statement.token_literal not 'let'. got={statement.token_literal()}")
        self.assertIsInstance(statement, LetStatement,
                              f"statement not {name}. got={statement}")
        self.assertEqual(statement.name.value, name,
                         f"statement.name.value not {name}. got={statement.name.value}")
        self.assertEqual(statement.name.token_literal(), name,
                         f"statement not {name}. got={statement.name.token_literal()}")

    def _check_parser_errors(self, parser: Parser):
        errors = parser.errors
        if len(errors) == 0:
            return False

        message = f"parser has {len(errors)} errors:\n"
        for error in errors:
            message += f"parser error: {error}\n"
        self.fail(message)

    def _test_integer_literal(self, integer_literal: IntegerLiteral, value: int) -> bool:
        self.assertIsInstance(integer_literal, IntegerLiteral,
                              f"integer_literal not IntegerLiteral. got={type(integer_literal)}")
        self.assertEqual(integer_literal.value, value,
                         f"integer_literal.value not {value}. got={integer_literal.value}")
        self.assertEqual(integer_literal.token_literal(), str(value),
                         f"integer_literal not {value}. got={integer_literal.token_literal()}")


if __name__ == '__main__':
    unittest.main()
