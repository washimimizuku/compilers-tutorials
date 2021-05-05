from monkey.ast import (
    Expression, PrefixExpression, InfixExpression,
    Identifier,
    IntegerLiteral,
    Statement, LetStatement, ReturnStatement, ExpressionStatement,
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
        self._test_identifier(identifier, "foobar")

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
        self._test_integer_literal(literal, 5)

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
            self._test_prefix_expression(expression, test[1], test[2])

    def test_parsing_infix_expressions(self):
        infix_tests = [
            ["5 + 5;", 5, "+", 5],
            ["5 - 5;", 5, "-", 5],
            ["5 * 5;", 5, "*", 5],
            ["5 / 5;", 5, "/", 5],
            ["5 > 5;", 5, ">", 5],
            ["5 < 5;", 5, "<", 5],
            ["5 == 5;", 5, "==", 5],
            ["5 != 5;", 5, "!=", 5],
        ]

        for test in infix_tests:
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
            self._test_infix_expression(expression, test[1], test[2], test[3])

    def test_operator_precedence_parsing(self):
        infix_tests = [
            ["-a * b", "((-a) * b)"],
            ["!-a", "(!(-a))"],
            ["a + b + c", "((a + b) + c)"],
            ["a + b - c", "((a + b) - c)"],
            ["a * b * c", "((a * b) * c)"],
            ["a * b / c", "((a * b) / c)"],
            ["a + b / c", "(a + (b / c))"],
            ["a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)"],
            ["3 + 4; -5 * 5", "(3 + 4)((-5) * 5)"],
            ["5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"],
            ["5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))"],
            ["3 + 4 * 5 == 3 * 1 + 4 * 5",
                "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"],
        ]

        for test in infix_tests:
            code = test[0]
            lexer = Lexer(code)
            parser = Parser(lexer)

            program = parser.parse_program()
            self._check_parser_errors(parser)

            self.assertEqual(
                str(program), test[1], f"expected={test[1]} got={str(program)}")

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

    def _test_prefix_expression(self, expression: PrefixExpression, operator, right):

        self.assertIsInstance(expression, PrefixExpression,
                              f"expression is not an instance of PrefixExpression. got={type(expression)}")
        self.assertEqual(expression.operator, operator,
                         f"expression.operator not {operator}. got={expression.operator}")
        self._test_integer_literal(expression.right, right)

    def _test_infix_expression(self, expression: InfixExpression, left, operator, right):
        self.assertIsInstance(expression, InfixExpression,
                              f"expression not InfixExpression. got={type(expression)}")
        self._test_literal_expression(expression.left, left)
        self.assertEqual(expression.operator, operator,
                         f"expression.operator not {operator}. got={expression.operator}")
        self._test_literal_expression(expression.right, right)

    def _test_literal_expression(self, expression: Expression, expected):
        if isinstance(expected, int):
            self._test_integer_literal(expression, expected)
        elif isinstance(expected, str):
            self._test_identifier(expression, expected)

    def _test_integer_literal(self, integer_literal: IntegerLiteral, value: int) -> None:
        self.assertIsInstance(integer_literal, IntegerLiteral,
                              f"integer_literal not IntegerLiteral. got={type(integer_literal)}")
        self.assertEqual(integer_literal.value, value,
                         f"integer_literal.value not {value}. got={integer_literal.value}")
        self.assertEqual(integer_literal.token_literal(), str(value),
                         f"integer_literal not {value}. got={integer_literal.token_literal()}")

    def _test_identifier(self, expression: Identifier, value: str) -> None:
        self.assertIsInstance(expression, Identifier,
                              f"expression not Identifier. got={type(expression)}")
        self.assertEqual(expression.value, value,
                         f"expression.value not {value}. got={expression.value}")
        self.assertEqual(expression.token_literal(), value,
                         f"expression.token_literal() not {value}. got={expression.token_literal()}")


if __name__ == '__main__':
    unittest.main()
