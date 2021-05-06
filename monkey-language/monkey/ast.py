import typing
from monkey.token import Token


class Node():
    def token_literal(self) -> str:
        raise NotImplementedError()

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        program = ""
        for statement in self.statements:
            program += str(statement)
        return program


class Identifier(Expression):
    def __init__(self, token: Token, value: str) -> None:
        self.token: Token = token
        self.value: str = value

    def expression_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return str(self.value)


class LetStatement(Statement):
    def __init__(self, token: Token) -> None:
        self.token: Token = token
        self.name: Identifier
        self.value: Expression

    def statement_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        statement = str(self.token_literal()) + " " + str(self.name) + " = "
        if self.value is not None:
            statement += str(self.value)
        statement += ";"
        return statement


class ReturnStatement(Statement):
    def __init__(self, token: Token) -> None:
        self.token: Token = token
        self.return_value: Expression

    def statement_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        statement = str(self.token_literal()) + " "
        if self.return_value is not None:
            statement += str(self.return_value)
        statement += ";"
        return statement


class ExpressionStatement(Statement):
    def __init__(self, token: Token) -> None:
        self.token: Token = token
        self.expression: Expression

    def statement_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        if self.expression is not None:
            return str(self.expression)
        else:
            return ""


class BlockStatement(Statement):
    def __init__(self, token: Token) -> None:
        self.token: Token = token
        self.statements: typing.List[Statement] = []

    def statement_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        result = ""
        for statement in statements:
            result += str(statement)

        return result


class IntegerLiteral(Expression):
    def __init__(self, token: Token) -> None:
        self.token: Token = token
        self.value: int

    def expression_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.token_literal()


class BooleanLiteral(Expression):
    def __init__(self, token: Token, value: bool) -> None:
        self.token: Token = token
        self.value: bool = value

    def expression_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.token_literal()


class FunctionLiteral(Expression):
    def __init__(self, token: Token) -> None:
        self.token: Token = token
        self.parameters: typing.List[Identifier] = []
        self.body: BlockStatement

    def expression_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        parameters = []
        for parameter in parameters:
            parameters.append(str(parameter))

        return f"{self.token_literal()} ( {parameters.join(', ')} ) {str(self.body)}"


class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: str) -> None:
        self.token: Token = token
        self.operator: str = operator
        self.right: Expression

    def expression_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({self.operator}{str(self.right)})"


class InfixExpression(Expression):
    def __init__(self, token: Token, operator: str, left: Expression) -> None:
        self.token: Token = token
        self.left: Expression = left
        self.operator: str = operator
        self.right: Expression

    def expression_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({str(self.left)} {self.operator} {str(self.right)})"


class IfExpression(Expression):
    def __init__(self, token: Token) -> None:
        self.token: Token = token
        self.condition: Expression
        self.consequence: BlockStatement
        self.alternative: BlockStatement

    def expression_node(self) -> None:
        # Just for debugging
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        result = f"if {str(self.condition)} {self.consequence}"
        if self.alternative is not None:
            result += f"else {str(self.alternative)} "
        return result
