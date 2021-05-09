import typing
import monkey.ast as ast
from monkey.object import Object, ObjectType, Integer


def evaluate(node: ast.Node) -> Object:
    # Statements
    if type(node) is ast.Program:
        return _eval_statements(node.statements)
    elif type(node) is ast.ExpressionStatement:
        return evaluate(node.expression)

    # Expressions
    elif type(node) is ast.IntegerLiteral:
        return Integer(node.value)
    else:
        return None


def _eval_statements(statements: typing.List[ast.Statement]) -> Object:
    result = None

    for statement in statements:
        result = evaluate(statement)

    return result
