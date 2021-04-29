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

        self.assertNotEqual(program, None)
        self.assertEqual(len(program.statements), 3)
        

if __name__ == '__main__':
    unittest.main()
