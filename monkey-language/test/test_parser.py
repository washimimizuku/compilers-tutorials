from monkey.ast import Statement, LetStatement
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
                         f"program.Statements does not contain 3 statements. got={len(program.statements)}")

        expected = ['x', 'y', 'foobar']
        for i in range(3):
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


if __name__ == '__main__':
    unittest.main()
