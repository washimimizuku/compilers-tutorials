from monkey.lexer import Lexer
from monkey.token import Token, TokenType

PROMPT = '>> '

def start() -> None:
    while True:
        line = input(PROMPT)
        lex = Lexer(line)

        tok = Token('', '')
        while tok.token_type != TokenType.EOF:
            tok = lex.next_token()
            print(tok)


if __name__ == "__main__":
    start()
    