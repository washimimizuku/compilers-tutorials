from monkey.ast import (
    Expression, PrefixExpression, InfixExpression, IfExpression, CallExpression, IndexExpression,
    Identifier,
    BooleanLiteral, IntegerLiteral, StringLiteral, FunctionLiteral, ArrayLiteral, HashLiteral,
    Statement, LetStatement, ReturnStatement, ExpressionStatement,
)
from monkey.lexer import Lexer
from monkey.parser import Parser
import unittest


class TestParser(unittest.TestCase):

    def test_parsing_let_statements(self):
        let_statements_tests = (
            ("let x = 5;", "x", 5),
            ("let y = true;", "y", True),
            ("let foobar = y;", "foobar", "y"),
        )

        for (code, expected_identifier, expected_value) in let_statements_tests:
            lexer = Lexer(code)
            parser = Parser(lexer)

            program = parser.parse_program()
            self._check_parser_errors(parser)

            self.assertEqual(len(program.statements), 1,
                             f"program.statements does not contain 1 statement. got={len(program.statements)}")

            statement = program.statements[0]
            self._test_let_statement(statement, expected_identifier)

            value = statement.value
            self._test_literal_expression(value, expected_value)

    def test_parsing_invalid_let_statements(self):
        let_statements_tests = [
            "let x 5;",
            "let = 10;",
            "let 838383;"
        ]

        for test in let_statements_tests:
            lexer = Lexer(test)
            parser = Parser(lexer)

            parser.parse_program()
            with self.assertRaises(AssertionError):
                self._check_parser_errors(parser)

    def test_parsing_return_statements(self):
        return_statements_tests = (
            ("return 5;", 5),
            ("return 10;", 10),
            ("return 993322;", 993322),
        )

        for (code, expected) in return_statements_tests:
            lexer = Lexer(code)
            parser = Parser(lexer)

            program = parser.parse_program()
            self._check_parser_errors(parser)

            self.assertEqual(len(program.statements), 1,
                             f"program.statements does not contain 1 statement. got={len(program.statements)}")

            statement = program.statements[0]
            self.assertIsInstance(statement, ReturnStatement,
                                  f"statement not 'return'. got={statement}")
            self.assertEqual(statement.token_literal(),
                             'return', f"statement.token_literal not 'return'. got={statement.token_literal()}")
            self.assertEqual(statement.return_value.value,
                             expected, f"statement.return_value not {expected}. got={statement.return_value.value}")

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
        boolean_literal_tests = (
            ("true;", True),
            ("false;", False)
        )

        for (code, expected) in boolean_literal_tests:
            lexer = Lexer(code)
            parser = Parser(lexer)

            program = parser.parse_program()
            self._check_parser_errors(parser)

            self.assertEqual(len(program.statements), 1,
                             f"program.statements does not contain 1 statement. got={len(program.statements)}")
            self.assertIsInstance(program.statements[0], ExpressionStatement,
                                  f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

            literal = program.statements[0].expression
            self._test_boolean_literal(literal, expected)

    def test_parsing_string_literal_expression(self):
        code = '"hello world";'
        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        literal = program.statements[0].expression
        self._test_string_literal(literal, 'hello world')

    def test_parsing_array_literal_expression(self):
        code = "[1, 2 * 2, 3 + 3]"
        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        expression = program.statements[0].expression
        self.assertIsInstance(expression, ArrayLiteral,
                              f"expression is not an instance of ArrayLiteral. got={type(expression)}")
        self.assertEqual(len(expression.elements), 3,
                         f"expression.elements does not contain 3 elements. got={len(expression.elements)}")
        self._test_integer_literal(expression.elements[0], 1)
        self._test_infix_expression(expression.elements[1], 2, '*', 2)
        self._test_infix_expression(expression.elements[2], 3, '+', 3)

    def test_parsing_hash_literal_string_keys(self):
        code = '{"one": 1, "two": 2, "three": 3}'
        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        hash_expression = program.statements[0].expression
        self.assertIsInstance(hash_expression, HashLiteral,
                              f"expression is not an instance of HashLiteral. got={type(hash_expression)}")
        self.assertEqual(len(hash_expression.pairs), 3,
                         f"hash.pairs does not contain 3 pairs. got={len(hash_expression.pairs)}")

        expected = {
            "one": 1,
            "two": 2,
            "three": 3,
        }
        for key, value in hash_expression.pairs.items():
            self.assertIsInstance(key, StringLiteral,
                                  f"key is not an instance of StringLiteral. got={type(key)}")
            self._test_integer_literal(value, expected[str(key)])

    def test_parsing_hash_literal_integer_keys(self):
        code = '{1: 1, 2: 2, 3: 3}'
        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        hash_expression = program.statements[0].expression
        self.assertIsInstance(hash_expression, HashLiteral,
                              f"expression is not an instance of HashLiteral. got={type(hash_expression)}")
        self.assertEqual(len(hash_expression.pairs), 3,
                         f"hash.pairs does not contain 3 pairs. got={len(hash_expression.pairs)}")

        expected = {
            1: 1,
            2: 2,
            3: 3,
        }
        for key, value in hash_expression.pairs.items():
            self.assertIsInstance(key, IntegerLiteral,
                                  f"key is not an instance of IntegerLiteral. got={type(key)}")
            self._test_integer_literal(value, expected[key.value])

    def test_parsing_hash_literal_boolean_keys(self):
        code = '{true: 1, false: 2}'
        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        hash_expression = program.statements[0].expression
        self.assertIsInstance(hash_expression, HashLiteral,
                              f"expression is not an instance of HashLiteral. got={type(hash_expression)}")
        self.assertEqual(len(hash_expression.pairs), 2,
                         f"hash.pairs does not contain 2 pairs. got={len(hash_expression.pairs)}")

        expected = {
            True: 1,
            False: 2,
        }
        for key, value in hash_expression.pairs.items():
            self.assertIsInstance(key, BooleanLiteral,
                                  f"key is not an instance of BooleanLiteral. got={type(key)}")
            self._test_integer_literal(value, expected[key.value])

    def test_parsing_empty_hash_literal(self):
        code = '{}'
        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        hash_expression = program.statements[0].expression
        self.assertIsInstance(hash_expression, HashLiteral,
                              f"expression is not an instance of HashLiteral. got={type(hash_expression)}")
        self.assertEqual(len(hash_expression.pairs), 0,
                         f"hash.pairs has wrong length. got={len(hash_expression.pairs)}")

    def test_parsing_hash_literals_with_expressions(self):
        code = '{"one": 0 + 1, "two": 10 - 8, "three": 15 / 5}'
        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        hash_expression = program.statements[0].expression
        self.assertIsInstance(hash_expression, HashLiteral,
                              f"expression is not an instance of HashLiteral. got={type(hash_expression)}")
        self.assertEqual(len(hash_expression.pairs), 3,
                         f"hash.pairs does not contain 3 pairs. got={len(hash_expression.pairs)}")

        tests = {
            "one": lambda exp: self._test_infix_expression(exp, 0, "+", 1),
            "two": lambda exp: self._test_infix_expression(exp, 10, "-", 8),
            "three": lambda exp: self._test_infix_expression(exp, 15, "/", 5),
        }

        for key, value in hash_expression.pairs.items():
            self.assertIsInstance(key, StringLiteral,
                                  f"key is not an instance of StringLiteral. got={type(key)}")
            test_function = tests[str(key)]
            test_function(value)

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
        function_parameters_tests = (
            ("fn() {};", []),
            ("fn(x) {};", ["x"]),
            ("fn(x, y, z) {};", ["x", "y", "z"]),
            ("fn(x,y,z){};", ["x", "y", "z"]),
        )

        for (code, expected) in function_parameters_tests:
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
            self.assertEqual(len(function.parameters), len(expected),
                             f"length of function.parameters is worng. want {len(expected)}, got={len(function.body.statements)}")

            for i in range(len(expected)):
                self._test_literal_expression(
                    function.parameters[i], expected[i])

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
        prefix_tests = (
            ("!5", "!", 5),
            ("-15", "-", 15),
            ("!true;", "!", True),
            ("!false;", "!", False),
        )

        for (code, expected_operator, expected_value) in prefix_tests:
            lexer = Lexer(code)
            parser = Parser(lexer)

            program = parser.parse_program()
            self._check_parser_errors(parser)

            self.assertEqual(len(program.statements), 1,
                             f"program.statements does not contain 1 statement. got={len(program.statements)}")
            self.assertIsInstance(program.statements[0], ExpressionStatement,
                                  f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

            expression = program.statements[0].expression
            self._test_prefix_expression(
                expression, expected_operator, expected_value)

    def test_parsing_infix_expressions(self):
        infix_tests = (
            ("5 + 5;", 5, "+", 5),
            ("5 - 5;", 5, "-", 5),
            ("5 * 5;", 5, "*", 5),
            ("5 / 5;", 5, "/", 5),
            ("5 > 5;", 5, ">", 5),
            ("5 < 5;", 5, "<", 5),
            ("5 == 5;", 5, "==", 5),
            ("5 != 5;", 5, "!=", 5),
            ("true == true", True, "==", True),
            ("true != false", True, "!=", False),
            ("false == false", False, "==", False),
        )

        for (code, expected_left_value, expected_operator, expected_right_value) in infix_tests:
            lexer = Lexer(code)
            parser = Parser(lexer)

            program = parser.parse_program()
            self._check_parser_errors(parser)

            self.assertEqual(len(program.statements), 1,
                             f"program.statements does not contain 1 statement. got={len(program.statements)}")
            self.assertIsInstance(program.statements[0], ExpressionStatement,
                                  f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

            expression = program.statements[0].expression
            self._test_infix_expression(
                expression, expected_left_value, expected_operator, expected_right_value)

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
        infix_tests = (
            ("-a * b", "((-a) * b)"),
            ("!-a", "(!(-a))"),
            ("a + b + c", "((a + b) + c)"),
            ("a + b - c", "((a + b) - c)"),
            ("a * b * c", "((a * b) * c)"),
            ("a * b / c", "((a * b) / c)"),
            ("a + b / c", "(a + (b / c))"),
            ("a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)"),
            ("3 + 4; -5 * 5", "(3 + 4)((-5) * 5)"),
            ("5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"),
            ("5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))"),
            ("3 + 4 * 5 == 3 * 1 + 4 * 5",
                "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),
            ("true", "true"),
            ("false", "false"),
            ("3 > 5 == false", "((3 > 5) == false)"),
            ("3 < 5 == true", "((3 < 5) == true)"),
            ("1 + (2 + 3) + 4", "((1 + (2 + 3)) + 4)"),
            ("(5 + 5) * 2", "((5 + 5) * 2)"),
            ("2 / (5 + 5)", "(2 / (5 + 5))"),
            ("-(5 + 5)", "(-(5 + 5))"),
            ("!(true == true)", "(!(true == true))"),
            ("a + add(b * c) + d", "((a + add((b * c))) + d)"),
            ("add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))",
             "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))"),
            ("add(a + b + c * d / f + g)",
             "add((((a + b) + ((c * d) / f)) + g))"),
            ("a * [1, 2, 3, 4][b * c] * d",
             "((a * ([1, 2, 3, 4][(b * c)])) * d)"),
            ("add(a * b[2], b[1], 2 * [1, 2][1])",
             "add((a * (b[2])), (b[1]), (2 * ([1, 2][1])))"),
        )

        for (code, expected) in infix_tests:
            lexer = Lexer(code)
            parser = Parser(lexer)

            program = parser.parse_program()
            self._check_parser_errors(parser)

            self.assertEqual(
                str(program), expected, f"expected={expected} got={str(program)}")

    def test_parsing_index_expressions(self):
        code = "myArray[1 + 1]"
        lexer = Lexer(code)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        self.assertEqual(len(program.statements), 1,
                         f"program.statements does not contain 1 statement. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        expression = program.statements[0].expression
        self.assertIsInstance(expression, IndexExpression,
                              f"expression is not an instance of IndexExpression. got={type(expression)}")
        self._test_identifier(expression.left, "myArray")
        self._test_infix_expression(expression.index, 1, "+", 1)

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

    def _test_string_literal(self, string_literal: StringLiteral, value: str) -> None:
        self.assertIsInstance(string_literal, StringLiteral,
                              f"string_literal not StringLiteral. got={type(string_literal)}")
        self.assertEqual(string_literal.value, value,
                         f"string_literal.value not {value}. got={string_literal.value}")
        self.assertEqual(string_literal.token_literal(), value,
                         f"string_literal not {value}. got={string_literal.token_literal()}")

    def _test_identifier(self, expression: Identifier, value: str) -> None:
        self.assertIsInstance(expression, Identifier,
                              f"expression not Identifier. got={type(expression)}")
        self.assertEqual(expression.value, value,
                         f"expression.value not {value}. got={expression.value}")
        self.assertEqual(expression.token_literal(), value,
                         f"expression.token_literal() not {value}. got={expression.token_literal()}")
