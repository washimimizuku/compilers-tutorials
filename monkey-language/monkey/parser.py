import enum
import typing

from monkey.token import Token, TokenType
from monkey.lexer import Lexer
from monkey.ast import (
    Program,
    Statement, LetStatement, ReturnStatement,
    Identifier,
    Expression, ExpressionStatement,
    IntegerLiteral
)


class Precedence(enum.Enum):
    LOWEST = 1
    EQUALS = 2       # ==
    LESSGREATER = 3  # > or <
    SUM = 4          # +
    PRODUCT = 5      # *
    PREFIX = 6       # -x or !x
    CALL = 7         # myFunction(x)


class Parser():
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.errors: typing.List[str] = []
        self.current_token = None
        self.peek_token = None
        self.prefix_parse_functions: typing.Dict[
            TokenType, typing.Callable[[], typing.Optional[Expression]]] = {}
        self.infix_parse_functions: typing.Dict[
            TokenType, typing.Callable[[Expression], typing.Optional[Expression]]] = {}

        # Read two tokens, so current_token and peek_token are both set
        self.next_token()
        self.next_token()

        # Register prefix functions
        self.register_prefix(TokenType.IDENT, self.parse_identifier)
        self.register_prefix(TokenType.INT, self.parse_integer_literal)

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
            return self.parse_expression_statement()

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

    def parse_expression_statement(self) -> ExpressionStatement:
        statement = ExpressionStatement(self.current_token)

        statement.expression = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return statement

    def parse_expression(self, precedence: Precedence) -> Expression:
        prefix = self.prefix_parse_functions[self.current_token.token_type]

        if prefix is not None:
            left_expression = prefix()
            return left_expression
        else:
            return None

    def parse_identifier(self) -> Expression:
        return Identifier(self.current_token, self.current_token.literal)

    def parse_integer_literal(self) -> Expression:
        literal = IntegerLiteral(self.current_token)

        try:
            value = int(self.current_token.literal)
        except ValueError:
            message = f"Could not parse {self.current_token.literal} as integer."
            self.errors.append(message)
            return None

        literal.value = value
        return literal

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

    def register_prefix(self, token_type: TokenType, function: typing.Callable[[], typing.Optional[Expression]]) -> None:
        self.prefix_parse_functions[token_type] = function

    def register_infix(self, token_type: TokenType, function: typing.Callable[[Expression], typing.Optional[Expression]]) -> None:
        self.infix_parse_functions[token_type] = function
