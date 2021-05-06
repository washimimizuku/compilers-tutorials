from monkey.ast import (
    Expression, PrefixExpression, InfixExpression, IfExpression, CallExpression,
    Identifier,
    BooleanLiteral, IntegerLiteral, FunctionLiteral,
    Statement, LetStatement, ReturnStatement, ExpressionStatement,
)
from monkey.lexer import Lexer
from monkey.parser import Parser
import unittest


class TestParser(unittest.TestCase):

    def test_parsing_let_statements(self):
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

    def test_parsing_invalid_let_statements(self):
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

    def test_parsing_return_statements(self):
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

    def test_parsing_identifier_expression(self):
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

    def test_parsing_integer_literal_expression(self):
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

    def test_parsing_boolean_literal_expression(self):
        boolean_literal_tests = [
            ["true;", True],
            ["false;", False]
        ]

        for test in boolean_literal_tests:
            code = test[0]
            lexer = Lexer(code)
            parser = Parser(lexer)

            program = parser.parse_program()
            self._check_parser_errors(parser)

            self.assertEqual(len(program.statements), 1,
                             f"program.statements does not contain 1 statement. got={len(program.statements)}")
            self.assertIsInstance(program.statements[0], ExpressionStatement,
                                  f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

            literal = program.statements[0].expression
            self._test_boolean_literal(literal, test[1])

    def test_parsing_function_literal_expression(self):
        code = "fn(x, y) { x + y; }"

        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")

        statement = program.statements[0]
        self.assertIsInstance(statement, ExpressionStatement,
                              f"statement is not an instance of ExpressionStatement. got={type(statement)}")
        function = statement.expression
        self.assertIsInstance(function, FunctionLiteral,
                              f"function is not an instance of FunctionLiteral. got={type(function)}")
        self.assertEqual(len(function.parameters), 2,
                         f"function literal parameters wrong. want 2,  got={len(function.parameters)}")

        self._test_literal_expression(function.parameters[0], "x")
        self._test_literal_expression(function.parameters[1], "y")

        self.assertEqual(len(function.body.statements), 1,
                         f"function.body.statements has not 1 statements, got={len(function.body.statements)}")

        body_statement = function.body.statements[0]
        self.assertIsInstance(body_statement, ExpressionStatement,
                              f"function body statement is not an instance of ExpressionStatement. got={type(body_statement)}")
        self._test_infix_expression(body_statement.expression, "x", "+", "y")

    def test_parsing_function_parameters(self):
        function_parameters_tests = [
            ["fn() {};", []],
            ["fn(x) {};", ["x"]],
            ["fn(x, y, z) {};", ["x", "y", "z"]],
            ["fn(x,y,z){};", ["x", "y", "z"]],
        ]

        for test in function_parameters_tests:
            code = test[0]
            lexer = Lexer(code)
            parser = Parser(lexer)

            program = parser.parse_program()
            self._check_parser_errors(parser)

            statement = program.statements[0]
            self.assertIsInstance(statement, ExpressionStatement,
                                  f"statement is not an instance of ExpressionStatement. got={type(statement)}")
            function = statement.expression
            self.assertIsInstance(function, FunctionLiteral,
                                  f"function is not an instance of FunctionLiteral. got={type(function)}")
            self.assertEqual(len(function.parameters), len(test[1]),
                             f"length of function.parameters is worng. want {len(test[1])}, got={len(function.body.statements)}")

            for i in range(len(test[1])):
                self._test_literal_expression(
                    function.parameters[i], test[1][i])

    def test_parsing_call_expression(self) -> None:
        code = "add(1, 2 * 3, 4 + 5);"

        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")

        statement = program.statements[0]
        self.assertIsInstance(statement, ExpressionStatement,
                              f"statement is not an instance of ExpressionStatement. got={type(statement)}")

        expression = statement.expression
        self.assertIsInstance(expression, CallExpression,
                              f"statement.expression is not an instance of CallExpression. got={type(expression)}")

        self._test_identifier(expression.function, "add")

        self.assertEqual(len(expression.arguments), 3,
                         f"wrong length of arguments. got={len(expression.arguments)}")

        self._test_literal_expression(expression.arguments[0], 1)
        self._test_infix_expression(expression.arguments[1],  2, "*", 3)
        self._test_infix_expression(expression.arguments[2],  4, "+", 5)

    def test_parsing_prefix_expressions(self):
        prefix_tests = [
            ["!5", "!", 5],
            ["-15", "-", 15],
            ["!true;", "!", True],
            ["!false;", "!", False],
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
            ["true == true", True, "==", True],
            ["true != false", True, "!=", False],
            ["false == false", False, "==", False],
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

    def test_parsing_if_expression(self):
        code = "if (x < y) { x }"

        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        expression = program.statements[0].expression
        self.assertIsInstance(expression, IfExpression,
                              f"statement.expression is not an instance of IfExpression. got={type(expression)}")

        self._test_infix_expression(expression.condition, "x", "<", "y")

        self.assertEqual(len(expression.consequence.statements), 1,
                         f"expression.consequence.statements does not contain 1 statement. got={len(expression.consequence.statements)}")

        consequence = expression.consequence
        self.assertIsInstance(consequence.statements[0], ExpressionStatement,
                              f"consequence.Statements[0] is not an instance of ExpressionStatement. got={type(consequence.statements[0])}")

        self._test_identifier(consequence.statements[0].expression, "x")

        if hasattr(expression, "alternative"):
            self.fail(
                f"expression.alternative is not None. got={(expression.alternative)}")

    def test_parsing_if_else_expression(self):
        code = "if (x < y) { x } else { y }"

        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        expression = program.statements[0].expression
        self.assertIsInstance(expression, IfExpression,
                              f"statement.expression is not an instance of IfExpression. got={type(expression)}")

        self._test_infix_expression(expression.condition, "x", "<", "y")

        self.assertEqual(len(expression.consequence.statements), 1,
                         f"expression.consequence.statements does not contain 1 statement. got={len(expression.consequence.statements)}")

        consequence = expression.consequence
        self.assertIsInstance(consequence.statements[0], ExpressionStatement,
                              f"consequence.Statements[0] is not an instance of ExpressionStatement. got={type(consequence.statements[0])}")

        self._test_identifier(consequence.statements[0].expression, "x")

        alternative = expression.alternative
        self.assertIsInstance(alternative.statements[0], ExpressionStatement,
                              f"alternative.Statements[0] is not an instance of ExpressionStatement. got={type(alternative.statements[0])}")

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
            ["true", "true"],
            ["false", "false"],
            ["3 > 5 == false", "((3 > 5) == false)"],
            ["3 < 5 == true", "((3 < 5) == true)"],
            ["1 + (2 + 3) + 4", "((1 + (2 + 3)) + 4)"],
            ["(5 + 5) * 2", "((5 + 5) * 2)"],
            ["2 / (5 + 5)", "(2 / (5 + 5))"],
            ["-(5 + 5)", "(-(5 + 5))"],
            ["!(true == true)", "(!(true == true))"],
        ]

        for test in infix_tests:
            code = test[0]
            lexer = Lexer(code)
            parser = Parser(lexer)

            program = parser.parse_program()
            self._check_parser_errors(parser)

            self.assertEqual(
                str(program), test[1], f"expected={test[1]} got={str(program)}")

    def _test_let_statement(self, statement: Statement, name: str) -> None:
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
        self._test_literal_expression(expression.right, right)

    def _test_infix_expression(self, expression: InfixExpression, left, operator, right):
        self.assertIsInstance(expression, InfixExpression,
                              f"expression not InfixExpression. got={type(expression)}")
        self._test_literal_expression(expression.left, left)
        self.assertEqual(expression.operator, operator,
                         f"expression.operator not {operator}. got={expression.operator}")
        self._test_literal_expression(expression.right, right)

    def _test_literal_expression(self, expression: Expression, expected):
        if isinstance(expected, bool):
            self._test_boolean_literal(expression, expected)
        elif isinstance(expected, int):
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

    def _test_boolean_literal(self, boolean_literal: BooleanLiteral, value: bool) -> None:
        self.assertIsInstance(boolean_literal, BooleanLiteral,
                              f"boolean_literal not BooleanLiteral. got={type(boolean_literal)}")
        self.assertEqual(boolean_literal.value, value,
                         f"boolean_literal.value not {value}. got={boolean_literal.value}")
        self.assertEqual(boolean_literal.token_literal(), str(value).lower(),
                         f"boolean_literal not {value}. got={boolean_literal.token_literal()}")

    def _test_identifier(self, expression: Identifier, value: str) -> None:
        self.assertIsInstance(expression, Identifier,
                              f"expression not Identifier. got={type(expression)}")
        self.assertEqual(expression.value, value,
                         f"expression.value not {value}. got={expression.value}")
        self.assertEqual(expression.token_literal(), value,
                         f"expression.token_literal() not {value}. got={expression.token_literal()}")
