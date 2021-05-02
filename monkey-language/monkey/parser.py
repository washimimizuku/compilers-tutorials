from monkey.ast import Program, Statement, LetStatement, ReturnStatement, Identifier
from monkey.lexer import Lexer
from monkey.token import Token, TokenType


class Parser():
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.errors = []
        self.current_token = None
        self.peek_token = None

        # Read two tokens, so current_token and peek_token are both set
        self.next_token()
        self.next_token()

    def next_token(self) -> None:
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self) -> Program:
        program = Program()
        program.statements = []

        while not self.current_token_is(TokenType.EOF):
            statement = self.parse_statement()
            if statement != None:
                program.statements.append(statement)
            self.next_token()

        return program

    def parse_statement(self) -> Statement:
        if self.current_token_is(TokenType.LET):
            return self.parse_let_statement()
        elif self.current_token_is(TokenType.RETURN):
            return self.parse_return_statement()
        else:
            return None

    def parse_let_statement(self) -> LetStatement:
        statement = LetStatement(self.current_token)

        if not self.expect_peek(TokenType.IDENT):
            return None

        statement.name = Identifier(
            self.current_token, self.current_token.literal)

        if not self.expect_peek(TokenType.ASSIGN):
            return None

        # TODO: We are skipping the expressions until we encounter a semicolon
        while not self.current_token_is(TokenType.SEMICOLON):
            self.next_token()

        return statement

    def parse_return_statement(self) -> ReturnStatement:
        statement = ReturnStatement(self.current_token)

        self.next_token()

        # TODO: We are skipping the expressions until we encounter a semicolon
        while not self.current_token_is(TokenType.SEMICOLON):
            self.next_token()

        return statement

    def current_token_is(self, token_type: TokenType) -> bool:
        return self.current_token.token_type == token_type

    def peek_token_is(self, token_type: TokenType) -> bool:
        return self.peek_token.token_type == token_type

    def expect_peek(self, token_type: TokenType) -> bool:
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        else:
            self.peek_error(token_type)
            return False

    def peek_error(self, token_type: TokenType):
        message = f"Expected next token to be {token_type}, got {self.peek_token.token_type} instead"
        self.errors.append(message)
