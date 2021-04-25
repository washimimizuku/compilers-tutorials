from lexer import BasicLexer
from parser import BasicParser
from interpreter import BasicInterpreter

if __name__ == "__main__":
    lexer = BasicLexer()
    parser = BasicParser()
    print("GFG Language")
    env = {}

    while True:

        try:
            text = input('GFG Language > ')
        
        except EOFError:
            break

        if text:
            tokens = lexer.tokenize(text)
            tree = parser.parse(tokens)
            BasicInterpreter(tree, env)
