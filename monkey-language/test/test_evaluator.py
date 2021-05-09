from monkey.evaluator import evaluate
from monkey.lexer import Lexer
from monkey.object import Object, Integer
from monkey.parser import Parser
import unittest


class TestEvaluator(unittest.TestCase):

    def test_eval_integer_expression(self):
        eval_integer_tests = (
            ("5", 5),
            ("10", 10),
        )

        for (code, expected) in eval_integer_tests:
            evaluated = self._test_eval(code)
            self._test_integer_object(evaluated, expected)

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
