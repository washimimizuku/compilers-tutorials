from monkey.environment import Environment
from monkey.evaluator import evaluate
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
    env = Environment()

    while True:
        line = input(PROMPT)

        lex = Lexer(line)
        pars = Parser(lex)

        program = pars.parse_program()
        if len(pars.errors) != 0:
            print_parser_errors(pars.errors)

        evaluated = evaluate(program, env)
        if evaluated != None:
            print(f"{str(evaluated.inspect())}")


def print_parser_errors(errors: str):
    for error in errors:
        print(MONKEY_FACE)
        print("Woops! We ran into some monkey business here!")
        print(" parser errors:")
        print(f"\t{error}")


if __name__ == "__main__":
    start()
