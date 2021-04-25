from sly import Lexer

class BasicLexer(Lexer):
    tokens = {
        NAME,
        NUMBER,
        STRING
    }
    ignore = '\t'
    literals = {'=', '+', '-', '/',
                '*', '(', ')', ',', ';'}


    # Define tokens as regular expressions
    # (stored as raw strings)
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'

    # Number token
    @_(r'\d+')
    def NUMBER(self, t):
        # Convert it into a python integer
        t.value = int(t.value)
        return t

    # Comment tokens
    @_(r'//.*')
    def COMMENT(self, t):
        pass
    
    # Newline token (used only for showing
    # errors in new line)
    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')
        