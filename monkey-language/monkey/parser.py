import enum
import typing

from monkey.token import Token, TokenType
from monkey.lexer import Lexer
from monkey.ast import (
    Program,
    Statement, LetStatement, ReturnStatement, BlockStatement,
    Identifier,
    Expression, ExpressionStatement, PrefixExpression, InfixExpression, IfExpression, CallExpression,
    BooleanLiteral, IntegerLiteral, FunctionLiteral,
)


class Precedence(enum.Enum):
    LOWEST = 1
    EQUALS = 2       # ==
    LESSGREATER = 3  # > or <
    SUM = 4          # +
    PRODUCT = 5      # *
    PREFIX = 6       # -x or !x
    CALL = 7         # myFunction(x)


PRECEDENCES = {
    TokenType.EQ: Precedence.EQUALS,
    TokenType.NOT_EQ: Precedence.EQUALS,
    TokenType.LT: Precedence.LESSGREATER,
    TokenType.GT: Precedence.LESSGREATER,
    TokenType.PLUS: Precedence.SUM,
    TokenType.MINUS: Precedence.SUM,
    TokenType.SLASH: Precedence.PRODUCT,
    TokenType.ASTERISK: Precedence.PRODUCT,
    TokenType.LPAREN: Precedence.CALL,
}


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
        self.register_prefix(TokenType.BANG, self.parse_prefix_expression)
        self.register_prefix(TokenType.MINUS, self.parse_prefix_expression)
        self.register_prefix(TokenType.TRUE, self.parse_boolean_literal)
        self.register_prefix(TokenType.FALSE, self.parse_boolean_literal)
        self.register_prefix(TokenType.LPAREN, self.parse_grouped_expression)
        self.register_prefix(TokenType.IF, self.parse_if_expression)
        self.register_prefix(TokenType.FUNCTION, self.parse_function_literal)

        # Register infix functions
        self.register_infix(TokenType.PLUS, self.parse_infix_expression)
        self.register_infix(TokenType.MINUS, self.parse_infix_expression)
        self.register_infix(TokenType.SLASH, self.parse_infix_expression)
        self.register_infix(TokenType.ASTERISK, self.parse_infix_expression)
        self.register_infix(TokenType.EQ, self.parse_infix_expression)
        self.register_infix(TokenType.NOT_EQ, self.parse_infix_expression)
        self.register_infix(TokenType.LT, self.parse_infix_expression)
        self.register_infix(TokenType.GT, self.parse_infix_expression)
        self.register_infix(TokenType.LPAREN, self.parse_call_expression)

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

        self.next_token()

        value = self.parse_expression(Precedence.LOWEST)
        if value is None:
            return None
        statement.value = value

        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return statement

    def parse_return_statement(self) -> ReturnStatement:
        statement = ReturnStatement(self.current_token)

        self.next_token()

        return_value = self.parse_expression(Precedence.LOWEST)
        if return_value is None:
            return None
        statement.return_value = return_value

        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return statement

    def parse_expression_statement(self) -> ExpressionStatement:
        statement = ExpressionStatement(self.current_token)

        statement.expression = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return statement

    def parse_block_statement(self) -> BlockStatement:
        block = BlockStatement(self.current_token)
        block.statements = []

        self.next_token()

        while not self.current_token_is(TokenType.RBRACE) and not self.current_token_is(TokenType.EOF):
            statement = self.parse_statement()
            if statement is not None:
                block.statements.append(statement)
            self.next_token()

        return block

    def parse_expression(self, precedence: Precedence) -> Expression:
        try:
            prefix = self.prefix_parse_functions[self.current_token.token_type]
        except KeyError:
            self.no_prefix_parse_function_error(self.current_token.token_type)
            return None

        left_expression = prefix()

        while (not self.peek_token_is(TokenType.SEMICOLON) and precedence.value < self.peek_precedence().value):
            try:
                infix = self.infix_parse_functions[self.peek_token.token_type]
            except KeyError:
                return left_expression

            self.next_token()

            left_expression = infix(left_expression)

        return left_expression

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

    def parse_boolean_literal(self) -> Expression:
        literal = BooleanLiteral(
            self.current_token, self.current_token_is(TokenType.TRUE))
        return literal

    def parse_function_literal(self) -> Expression:
        literal = FunctionLiteral(self.current_token)

        if not self.expect_peek(TokenType.LPAREN):
            return None

        literal.parameters = self.parse_function_parameters()

        if not self.expect_peek(TokenType.LBRACE):
            return None

        literal.body = self.parse_block_statement()

        return literal

    def parse_function_parameters(self) -> typing.List[Identifier]:
        identifiers: typing.List[Identifier] = []

        if self.peek_token_is(TokenType.RPAREN):
            self.next_token()
            return identifiers

        self.next_token()

        identifier = Identifier(self.current_token, self.current_token.literal)
        identifiers.append(identifier)

        while self.peek_token_is(TokenType.COMMA):
            self.next_token()
            self.next_token()

            identifier = Identifier(
                self.current_token, self.current_token.literal)
            identifiers.append(identifier)

        if not self.expect_peek(TokenType.RPAREN):
            return None

        return identifiers

    def parse_prefix_expression(self) -> Expression:
        expression = PrefixExpression(
            self.current_token, self.current_token.literal)

        self.next_token()

        expression.right = self.parse_expression(Precedence.PREFIX)

        return expression

    def parse_infix_expression(self, left: Expression) -> Expression:
        expression = InfixExpression(
            self.current_token, self.current_token.literal, left)

        precedence = self.current_precedence()
        self.next_token()
        expression.right = self.parse_expression(precedence)

        return expression

    def parse_grouped_expression(self) -> Expression:
        self.next_token()

        expression = self.parse_expression(Precedence.LOWEST)

        if not self.expect_peek(TokenType.RPAREN):
            return None

        return expression

    def parse_if_expression(self) -> Expression:
        expression = IfExpression(self.current_token)

        if not self.expect_peek(TokenType.LPAREN):
            return None

        self.next_token()
        expression.condition = self.parse_expression(Precedence.LOWEST)

        if not self.expect_peek(TokenType.RPAREN):
            return None

        if not self.expect_peek(TokenType.LBRACE):
            return None

        expression.consequence = self.parse_block_statement()

        if self.peek_token_is(TokenType.ELSE):
            self.next_token()

            if not self.expect_peek(TokenType.LBRACE):
                return None

            expression.alternative = self.parse_block_statement()

        return expression

    def parse_call_expression(self, function: Expression) -> Expression:
        expression = CallExpression(self.current_token, function)
        expression.arguments = self.parse_call_arguments()
        return expression

    def parse_call_arguments(self) -> typing.List[Expression]:
        arguments: typing.List[Expression] = []

        if self.peek_token_is(TokenType.RPAREN):
            self.next_token()
            return arguments

        self.next_token()
        arguments.append(self.parse_expression(Precedence.LOWEST))

        while self.peek_token_is(TokenType.COMMA):
            self.next_token()
            self.next_token()
            arguments.append(self.parse_expression(Precedence.LOWEST))

        if not self.expect_peek(TokenType.RPAREN):
            return None

        return arguments

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
        message = f"Expected next token to be {token_type.value}, got {self.peek_token.token_type.value} instead"
        self.errors.append(message)

    def register_prefix(self, token_type: TokenType, function: typing.Callable[[], typing.Optional[Expression]]) -> None:
        self.prefix_parse_functions[token_type] = function

    def register_infix(self, token_type: TokenType, function: typing.Callable[[Expression], typing.Optional[Expression]]) -> None:
        self.infix_parse_functions[token_type] = function

    def no_prefix_parse_function_error(self, token_type: TokenType):
        message = f"no prefix parse function for {token_type.value} found"
        self.errors.append(message)

    def peek_precedence(self) -> int:
        try:
            precedence = PRECEDENCES[self.peek_token.token_type]
        except KeyError:
            return Precedence.LOWEST

        return precedence

    def current_precedence(self) -> int:
        try:
            precedence = PRECEDENCES[self.current_token.token_type]
        except KeyError:
            return Precedence.LOWEST

        return precedence
