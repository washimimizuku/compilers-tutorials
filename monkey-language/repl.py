from monkey.lexer import Lexer
from monkey.parser import Parser
from monkey.token import Token, TokenType

PROMPT = '>> '
MONKEY_FACE = '''
            __,__
   .--.  .-"     "-.  .--.
  / .. \/  .-. .-.  \/ .. \\
 | |  '|  /   Y   \  |'  | |
 | \   \  \ 0 | 0 /  /   / |
  \ '- ,\.-"`` ``"-./, -' /
   `'-' /_   ^ ^   _\ '-'`
       |  \._   _./  |
       \   \ `~` /   /
        '._ '-=-' _.'
           '~---~'
'''


def start() -> None:
    while True:
        line = input(PROMPT)

        lex = Lexer(line)
        pars = Parser(lex)
        program = pars.parse_program()

        if len(pars.errors) != 0:
            print_parser_errors(pars.errors)
        else:
            print(f"{str(program)}")


def print_parser_errors(errors: str):
    for error in errors:
        print(MONKEY_FACE)
        print("Woops! We ran into some monkey business here!")
        print(" parser errors:")
        print(f"\t{error}")


if __name__ == "__main__":
    start()
