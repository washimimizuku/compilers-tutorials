from monkey.environment import Environment
from monkey.evaluator import evaluate, NULL
from monkey.lexer import Lexer
from monkey.object import ObjectType, Object, Integer, Boolean, String, Error, Function, Array
from monkey.parser import Parser
import unittest


class TestEvaluator(unittest.TestCase):

    def test_eval_integer_expression(self):
        eval_integer_tests = (
            ("5", 5),
            ("10", 10),
            ("-5", -5),
            ("-10", -10),
            ("5 + 5 + 5 + 5 - 10", 10),
            ("2 * 2 * 2 * 2 * 2", 32),
            ("-50 + 100 + -50", 0),
            ("5 * 2 + 10", 20),
            ("5 + 2 * 10", 25),
            ("20 + 2 * -10", 0),
            ("50 / 2 * 2 + 10", 60),
            ("2 * (5 + 10)", 30),
            ("3 * 3 * 3 + 10", 37),
            ("3 * (3 * 3) + 10", 37),
            ("(5 + 10 * 2 + 15 / 3) * 2 + -10", 50),
        )

        for (code, expected) in eval_integer_tests:
            evaluated = self._test_eval(code)
            self._test_integer_object(evaluated, expected)

    def test_eval_boolean_expression(self):
        eval_boolean_tests = (
            ("true", True),
            ("false", False),
            ("1 < 2", True),
            ("1 > 2", False),
            ("1 < 1", False),
            ("1 > 1", False),
            ("1 == 1", True),
            ("1 != 1", False),
            ("1 == 2", False),
            ("1 != 2", True),
            ("true == true", True),
            ("false == false", True),
            ("true == false", False),
            ("true != false", True),
            ("false != true", True),
            ("(1 < 2) == true", True),
            ("(1 < 2) == false", False),
            ("(1 > 2) == true", False),
            ("(1 > 2) == false", True),
        )

        for (code, expected) in eval_boolean_tests:
            evaluated = self._test_eval(code)
            self._test_boolean_object(evaluated, expected)

    def test_if_else_expressions(self):
        eval_if_else_expressions = (
            ("if (true) { 10 }", 10),
            ("if (false) { 10 }", None),
            ("if (1) { 10 }", 10),
            ("if (1 < 2) { 10 }", 10),
            ("if (1 > 2) { 10 }", None),
            ("if (1 > 2) { 10 } else { 20 }", 20),
            ("if (1 < 2) { 10 } else { 20 }", 10),
        )

        for (code, expected) in eval_if_else_expressions:
            evaluated = self._test_eval(code)
            if isinstance(expected, int):
                self._test_integer_object(evaluated, expected)
            else:
                self._test_null_object(evaluated)

    def test_bang_operator(self):
        eval_boolean_tests = (
            ("!true", False),
            ("!false", True),
            ("!5", False),
            ("!!true", True),
            ("!!false", False),
            ("!!5", True),
        )

        for (code, expected) in eval_boolean_tests:
            evaluated = self._test_eval(code)
            self._test_boolean_object(evaluated, expected)

    def test_return_statement(self):
        eval_return_statement_tests = (
            ("return 10;", 10),
            ("return 10; 9;", 10),
            ("return 2 * 5; 9;", 10),
            ("9; return 2 * 5; 9;", 10),
            (
                '''
                if (10 > 1) {
                    if (10 > 1) {
                        return 10;
                    }
                    return 1;
                }
                ''',
                10
            ),
        )

        for (code, expected) in eval_return_statement_tests:
            evaluated = self._test_eval(code)
            self._test_integer_object(evaluated, expected)

    def test_let_statement(self):
        eval_let_statement_tests = (
            ("let a = 5; a;", 5),
            ("let a = 5 * 5; a;", 25),
            ("let a = 5; let b = a; b;", 5),
            ("let a = 5; let b = a; let c = a + b + 5; c;", 15),
        )

        for (code, expected) in eval_let_statement_tests:
            evaluated = self._test_eval(code)
            self._test_integer_object(evaluated, expected)

    def test_error_handling(self):
        error_handling_tests = (
            (
                "5 + true;",
                "type mismatch: ObjectType.INTEGER + ObjectType.BOOLEAN",
            ),
            (
                "5 + true; 5;",
                "type mismatch: ObjectType.INTEGER + ObjectType.BOOLEAN",
            ),
            (
                "-true",
                "unknown operator: -ObjectType.BOOLEAN",
            ),
            (
                "true + false;",
                "unknown operator: ObjectType.BOOLEAN + ObjectType.BOOLEAN",
            ),
            (
                "5; true + false; 5",
                "unknown operator: ObjectType.BOOLEAN + ObjectType.BOOLEAN",
            ),
            (
                "if (10 > 1) { true + false; }",
                "unknown operator: ObjectType.BOOLEAN + ObjectType.BOOLEAN",
            ),
            (
                '''
                if (10 > 1) {
                    if (10 > 1) {
                        return true + false;
                    }
                    return 1;
                }
                ''',
                "unknown operator: ObjectType.BOOLEAN + ObjectType.BOOLEAN"
            ),
            (
                "foobar",
                "identifier not found: foobar",
            ),
            (
                '"Hello" - "World"',
                "unknown operator: ObjectType.STRING - ObjectType.STRING",
            ),
        )

        for (code, expected) in error_handling_tests:
            evaluated = self._test_eval(code)
            self.assertIsInstance(evaluated, Error,
                                  f"no error object returned. got={type(evaluated)}")
            self.assertEqual(evaluated.message, expected,
                             f"wrong error message. got={evaluated.message}, expected={expected}")

    def test_function_object(self):
        code = "fn(x) { x + 2; };"
        evaluated = self._test_eval(code)
        self.assertIsInstance(evaluated, Function,
                              f"object is not a function. got={type(evaluated)}")
        self.assertEqual(len(evaluated.parameters), 1,
                         f"function has wrong parameters. Parameters={len(evaluated.parameters)}")
        self.assertEqual(str(evaluated.parameters[0]), 'x',
                         f"parameter is not 'x'. got=={evaluated.parameters[0]}")

        expected_body = "(x + 2)"
        self.assertEqual(str(evaluated.body), expected_body,
                         f"body is not {expected_body}. got=={evaluated.body}")

    def test_function_application(self):
        function_application_tests = (
            ("let identity = fn(x) { x; }; identity(5);", 5),
            ("let identity = fn(x) { return x; }; identity(5);", 5),
            ("let double = fn(x) { x * 2; }; double(5);", 10),
            ("let add = fn(x, y) { x + y; }; add(5, 5);", 10),
            ("let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", 20),
            ("fn(x) { x; }(5)", 5),
        )

        for (code, expected) in function_application_tests:
            evaluated = self._test_eval(code)
            self._test_integer_object(evaluated, expected)

    def test_closures(self):
        code = '''
            let newAdder = fn(x) {
                fn(y) { x + y };
            };
            let addTwo = newAdder(2);
            addTwo(2);
        '''
        evaluated = self._test_eval(code)
        self._test_integer_object(evaluated, 4)

    def test_eval_string_literal(self):
        code = '"Hello World!"'
        evaluated = self._test_eval(code)

        expected = 'Hello World!'
        self.assertIsInstance(evaluated, String,
                              f"object is not String. got={type(evaluated)}")
        self.assertEqual(evaluated.value, expected,
                         f"object has wrong value. got={evaluated.value}, want={expected}")

    def test_eval_string_contatenation(self):
        code = '"Hello" + " " + "World!"'
        evaluated = self._test_eval(code)

        expected = 'Hello World!'
        self.assertIsInstance(evaluated, String,
                              f"object is not String. got={type(evaluated)}")
        self.assertEqual(evaluated.value, expected,
                         f"object has wrong value. got={evaluated.value}, want={expected}")

    def test_builtin_function_len(self):
        builtin_functions_tests = (
            ('len("")', 0),
            ('len("four")', 4),
            ('len("hello world")', 11),
            ('len(1)', "argument to 'len' not supported, got=ObjectType.INTEGER"),
            ('len("one", "two")', "wrong number of arguments. got=2, want=1"),
            ('len([])', 0),
            ('len([1, 2, 3])', 3),
            ('len([1, "hello", true])', 3),
        )

        for (code, expected) in builtin_functions_tests:
            evaluated = self._test_eval(code)

            if type(expected) is int:
                self._test_integer_object(evaluated, expected)
            elif type(expected) is str:
                self.assertIsInstance(evaluated, Error,
                                      f"object is not Error. got={type(evaluated)}")
                self.assertEqual(evaluated.message, expected,
                                 f"wrong error message. got={evaluated}, expected={expected}")

    def test_builtin_function_first(self):
        builtin_functions_tests = (
            ('first([])', NULL),
            ('first([1, 2, 3])', 1),
            ('first(["hello", 1, true])', 'hello'),
            ('first("foobar")', Error(
                "argument to 'first' must be ObjectType.ARRAY, got ObjectType.STRING")),
        )

        for (code, expected) in builtin_functions_tests:
            evaluated = self._test_eval(code)

            if type(expected) is int:
                self._test_integer_object(evaluated, expected)
            elif type(expected) is str:
                self.assertEqual(evaluated.value, expected,
                                 f"wrong string value. got={evaluated}, expected={expected}")
            elif expected.object_type() == ObjectType.NULL:
                self.assertEqual(evaluated.object_type(), expected.object_type(),
                                 f"wrong null value. got={evaluated.object_type()}, expected={expected.object_type()}")
            else:
                self.assertIsInstance(evaluated, Error,
                                      f"object is not Error. got={type(evaluated)}")
                self.assertEqual(evaluated.message, expected.message,
                                 f"wrong error message. got={evaluated}, expected={expected}")

    def test_builtin_function_last(self):
        builtin_functions_tests = (
            ('last([])', NULL),
            ('last([1, 2, 3])', 3),
            ('last([1, true, "hello"])', 'hello'),
            ('last("foobar")', Error(
                "argument to 'last' must be ObjectType.ARRAY, got ObjectType.STRING")),
        )

        for (code, expected) in builtin_functions_tests:
            evaluated = self._test_eval(code)

            if type(expected) is int:
                self._test_integer_object(evaluated, expected)
            elif type(expected) is str:
                self.assertEqual(evaluated.value, expected,
                                 f"wrong string value. got={evaluated}, expected={expected}")
            elif expected.object_type() == ObjectType.NULL:
                self.assertEqual(evaluated.object_type(), expected.object_type(),
                                 f"wrong null value. got={evaluated.object_type()}, expected={expected.object_type()}")
            else:
                self.assertIsInstance(evaluated, Error,
                                      f"object is not Error. got={type(evaluated)}")
                self.assertEqual(evaluated.message, expected.message,
                                 f"wrong error message. got={evaluated}, expected={expected}")

    def test_builtin_function_rest(self):
        builtin_functions_tests = (
            ('rest([])', NULL),
            ('rest([1, 2, 3])', [2, 3]),
            ('rest([1, true, "hello"])', [True, 'hello']),
            ('rest("foobar")', Error(
                "argument to 'rest' must be ObjectType.ARRAY, got ObjectType.STRING")),
        )

        for (code, expected) in builtin_functions_tests:
            evaluated = self._test_eval(code)

            if type(expected) is list:
                for index in range(len(evaluated)):

                    if type(expected) is int:
                        self._test_integer_object(
                            evaluated[index], expected[index])
                    elif type(expected) is bool:
                        self._test_boolean_object(
                            evaluated[index], expected[index])
                    elif type(expected) is str:
                        self.assertEqual(evaluated[index].value, expected[index],
                                         f"wrong string value. got={evaluated[index]}, expected={expected[index]}")
            elif expected.object_type() == ObjectType.NULL:
                self.assertEqual(evaluated.object_type(), expected.object_type(),
                                 f"wrong null value. got={evaluated.object_type()}, expected={expected.object_type()}")
            else:
                self.assertIsInstance(evaluated, Error,
                                      f"object is not Error. got={type(evaluated)}")
                self.assertEqual(evaluated.message, expected.message,
                                 f"wrong error message. got={evaluated}, expected={expected}")

    def test_array_literals(self):
        code = "[1, 2 * 2, 3 + 3]"
        evaluated = self._test_eval(code)

        self.assertIsInstance(evaluated, Array,
                              f"object is not Array. got={type(evaluated)}")
        self.assertEqual(len(evaluated.elements), 3,
                         f"array has wrong num of elements. got={len(evaluated.elements)}, expected=3")

        self._test_integer_object(evaluated.elements[0], 1)
        self._test_integer_object(evaluated.elements[1], 4)
        self._test_integer_object(evaluated.elements[2], 6)

    def test_array_index_expressions(self):
        builtin_functions_tests = (
            ("[1, 2, 3][0]", 1),
            ("[1, 2, 3][1]", 2),
            ("[1, 2, 3][2]", 3),
            ("let i = 0; [1][i];", 1),
            ("[1, 2, 3][1 + 1];", 3),
            ("let myArray = [1, 2, 3]; myArray[2];", 3),
            ("let myArray = [1, 2, 3]; myArray[0] + myArray[1] + myArray[2];", 6),
            ("let myArray = [1, 2, 3]; let i = myArray[0]; myArray[i]", 2),
            ("[1, 2, 3][3]", None),
            ("[1, 2, 3][-1]", None),
        )

        for (code, expected) in builtin_functions_tests:
            evaluated = self._test_eval(code)

            if type(expected) is int:
                self._test_integer_object(evaluated, expected)
            else:
                self._test_null_object(evaluated)

    def _test_eval(self, code):
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        env = Environment()

        return evaluate(program, env)

    def _test_integer_object(self, evaluated, expected):
        self.assertIsInstance(evaluated, Integer,
                              f"object is not Integer. got={type(evaluated)}")
        self.assertEqual(evaluated.value, expected,
                         f"object has wrong value. got={evaluated.value}, want={expected}")

    def _test_boolean_object(self, evaluated, expected):
        self.assertIsInstance(evaluated, Boolean,
                              f"object is not Boolean. got={type(evaluated)}")
        self.assertEqual(evaluated.value, expected,
                         f"object has wrong value. got={evaluated.value}, want={expected}")

    def _test_null_object(self, evaluated):
        self.assertEqual(
            evaluated, NULL, f"object is not NULL. got={evaluated.value}")
