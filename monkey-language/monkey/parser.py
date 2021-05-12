import enum
import typing

from monkey.token import Token, TokenType
from monkey.lexer import Lexer
import monkey.ast as ast


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
            TokenType, typing.Callable[[], typing.Optional[ast.Expression]]] = {}
        self.infix_parse_functions: typing.Dict[
            TokenType, typing.Callable[[ast.Expression], typing.Optional[ast.Expression]]] = {}

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
        self.register_prefix(TokenType.STRING, self.parse_string_literal)
        self.register_prefix(TokenType.LBRACKET, self.parse_array_literal)

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

    def parse_program(self) -> ast.Program:
        program = ast.Program()
        program.statements = []

        while not self.current_token_is(TokenType.EOF):
            statement = self.parse_statement()
            if statement != None:
                program.statements.append(statement)
            self.next_token()

        return program

    def parse_statement(self) -> ast.Statement:
        if self.current_token_is(TokenType.LET):
            return self.parse_let_statement()
        elif self.current_token_is(TokenType.RETURN):
            return self.parse_return_statement()
        else:
            return self.parse_expression_statement()

    def parse_let_statement(self) -> ast.LetStatement:
        statement = ast.LetStatement(self.current_token)

        if not self.expect_peek(TokenType.IDENT):
            return None

        statement.name = ast.Identifier(
            self.current_token, self.current_token.literal)

        if not self.expect_peek(TokenType.ASSIGN):
            return None

        self.next_token()

        statement.value = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return statement

    def parse_return_statement(self) -> ast.ReturnStatement:
        statement = ast.ReturnStatement(self.current_token)

        self.next_token()

        statement.return_value = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return statement

    def parse_expression_statement(self) -> ast.ExpressionStatement:
        statement = ast.ExpressionStatement(self.current_token)

        statement.expression = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return statement

    def parse_block_statement(self) -> ast.BlockStatement:
        block = ast.BlockStatement(self.current_token)
        block.statements = []

        self.next_token()

        while not self.current_token_is(TokenType.RBRACE) and not self.current_token_is(TokenType.EOF):
            statement = self.parse_statement()
            if statement is not None:
                block.statements.append(statement)
            self.next_token()

        return block

    def parse_expression(self, precedence: Precedence) -> ast.Expression:
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

    def parse_identifier(self) -> ast.Expression:
        return ast.Identifier(self.current_token, self.current_token.literal)

    def parse_integer_literal(self) -> ast.Expression:
        literal = ast.IntegerLiteral(self.current_token)

        try:
            value = int(self.current_token.literal)
        except ValueError:
            message = f"Could not parse {self.current_token.literal} as integer."
            self.errors.append(message)
            return None

        literal.value = value
        return literal

    def parse_boolean_literal(self) -> ast.Expression:
        literal = ast.BooleanLiteral(
            self.current_token, self.current_token_is(TokenType.TRUE))
        return literal

    def parse_string_literal(self) -> ast.Expression:
        return ast.StringLiteral(self.current_token, self.current_token.literal)

    def parse_array_literal(self) -> ast.Expression:
        array = ast.ArrayLiteral(self.current_token)
        array.elements = self.parse_expression_list(TokenType.RBRACKET)
        return array

    def parse_function_literal(self) -> ast.Expression:
        literal = ast.FunctionLiteral(self.current_token)

        if not self.expect_peek(TokenType.LPAREN):
            return None

        literal.parameters = self.parse_function_parameters()

        if not self.expect_peek(TokenType.LBRACE):
            return None

        literal.body = self.parse_block_statement()

        return literal

    def parse_function_parameters(self) -> typing.List[ast.Identifier]:
        identifiers: typing.List[ast.Identifier] = []

        if self.peek_token_is(TokenType.RPAREN):
            self.next_token()
            return identifiers

        self.next_token()

        identifier = ast.Identifier(
            self.current_token, self.current_token.literal)
        identifiers.append(identifier)

        while self.peek_token_is(TokenType.COMMA):
            self.next_token()
            self.next_token()

            identifier = ast.Identifier(
                self.current_token, self.current_token.literal)
            identifiers.append(identifier)

        if not self.expect_peek(TokenType.RPAREN):
            return None

        return identifiers

    def parse_prefix_expression(self) -> ast.Expression:
        expression = ast.PrefixExpression(
            self.current_token, self.current_token.literal)

        self.next_token()

        expression.right = self.parse_expression(Precedence.PREFIX)

        return expression

    def parse_infix_expression(self, left: ast.Expression) -> ast.Expression:
        expression = ast.InfixExpression(
            self.current_token, self.current_token.literal, left)

        precedence = self.current_precedence()
        self.next_token()
        expression.right = self.parse_expression(precedence)

        return expression

    def parse_grouped_expression(self) -> ast.Expression:
        self.next_token()

        expression = self.parse_expression(Precedence.LOWEST)

        if not self.expect_peek(TokenType.RPAREN):
            return None

        return expression

    def parse_if_expression(self) -> ast.Expression:
        expression = ast.IfExpression(self.current_token)

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

    def parse_call_expression(self, function: ast.Expression) -> ast.Expression:
        expression = ast.CallExpression(self.current_token, function)
        expression.arguments = self.parse_expression_list(TokenType.RPAREN)
        return expression

    def parse_expression_list(self, end: TokenType) -> typing.List[ast.Expression]:
        expression_list: typing.List[ast.Expression] = []

        if self.peek_token_is(end):
            self.next_token()
            return expression_list

        self.next_token()
        expression_list.append(self.parse_expression(Precedence.LOWEST))

        while self.peek_token_is(TokenType.COMMA):
            self.next_token()
            self.next_token()
            expression_list.append(self.parse_expression(Precedence.LOWEST))

        if not self.expect_peek(end):
            return None

        return expression_list

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

    def register_prefix(self, token_type: TokenType, function: typing.Callable[[], typing.Optional[ast.Expression]]) -> None:
        self.prefix_parse_functions[token_type] = function

    def register_infix(self, token_type: TokenType, function: typing.Callable[[ast.Expression], typing.Optional[ast.Expression]]) -> None:
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
