import typing
from monkey.token import Token


class Node():
    def token_literal(self) -> str:
        raise NotImplementedError()


class Statement(Node):
    def statement_node(self) -> None:
        # Just for debugging
        pass


class Expression(Node):
    def expression_node(self) -> None:
        # Just for debugging
        pass


class Program():
    def __init__(self) -> None:
        self.statements: typing.List[Statement] = []

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            self.statements[0].token_literal()
        else:
            return ''


class Identifier(Expression):
    def __init__(self, token: Token, value: str) -> None:
        self.token = token
        self.value = value

    def expression_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal


class LetStatement(Statement):
    def __init__(self, token:Token) -> None:
        self.token = token
        self.name: Identifier
        self.value: Expression

    def statement_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal
