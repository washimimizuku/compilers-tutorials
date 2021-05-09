from monkey.evaluator import evaluate
from monkey.lexer import Lexer
from monkey.object import Object, Integer, Boolean
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

    def _test_eval(self, code):
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()

        return evaluate(program)

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
