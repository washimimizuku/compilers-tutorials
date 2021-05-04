from monkey.ast import Statement, LetStatement, ReturnStatement, ExpressionStatement, Identifier
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

        with self.assertRaises(KeyError):
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
                         f"program.statements does not contain 1 statements. got={len(program.statements)}")
        self.assertIsInstance(program.statements[0], ExpressionStatement,
                              f"program.Statements[0] is not an instance of ExpressionStatement. got={type(program.statements[0])}")

        identifier = program.statements[0].expression
        self.assertIsInstance(identifier, Identifier,
                              f"expression is not an instance of Identifier. got={type(identifier)}")
        self.assertEqual(identifier.value, "foobar",
                         f"identifier.value not foobar. got={identifier.value}")
        self.assertEqual(identifier.token_literal(), "foobar",
                         f"identifier.token_literal() not foobar. got={identifier.token_literal()}")

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
