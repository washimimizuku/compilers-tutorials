import typing
import monkey.ast as ast
from monkey.object import (
    Object, ObjectType,
    Integer, Boolean, Null
)

TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()


def evaluate(node: ast.Node) -> Object:
    # Statements
    if type(node) is ast.Program:
        return _eval_statements(node.statements)
    elif type(node) is ast.ExpressionStatement:
        return evaluate(node.expression)

    # Expressions
    elif type(node) is ast.IntegerLiteral:
        return Integer(node.value)
    elif type(node) is ast.BooleanLiteral:
        return _native_bool_to_boolean_object(node.value)
    elif type(node) is ast.PrefixExpression:
        right = evaluate(node.right)
        return _eval_prefix_expression(node.operator, right)
    else:
        return None


def _eval_statements(statements: typing.List[ast.Statement]) -> Object:
    result = None

    for statement in statements:
        result = evaluate(statement)

    return result


def _native_bool_to_boolean_object(input: bool) -> Boolean:
    if input:
        return TRUE
    else:
        return FALSE


def _eval_prefix_expression(operator: str, right: Object) -> Object:
    if operator == "!":
        return _eval_bang_operator_expression(right)
    elif operator == "-":
        return _eval_minus_prefix_operator_expression(right)
    else:
        return NULL


def _eval_bang_operator_expression(right: Object) -> Object:
    if right == TRUE:
        return FALSE
    elif right == FALSE:
        return TRUE
    elif right == NULL:
        return TRUE
    else:
        return FALSE


def _eval_minus_prefix_operator_expression(right: Object) -> Object:
    if right.object_type() != ObjectType.INTEGER:
        return NULL

    value = right.value
    return Integer(-value)
