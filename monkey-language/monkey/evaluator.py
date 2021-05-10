import typing
import monkey.ast as ast
from monkey.object import (
    Object, ObjectType,
    Integer, Boolean, Null, ReturnValue, Error,
)

TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()


def evaluate(node: ast.Node) -> Object:
    # Statements
    if type(node) is ast.Program:
        return _eval_program(node)
    elif type(node) is ast.ExpressionStatement:
        return evaluate(node.expression)
    elif type(node) is ast.BlockStatement:
        return _eval_block_statement(node)
    elif type(node) is ast.ReturnStatement:
        value = evaluate(node.return_value)

        if _is_error(value):
            return value
        return ReturnValue(value)

    # Expressions
    elif type(node) is ast.IntegerLiteral:
        return Integer(node.value)
    elif type(node) is ast.BooleanLiteral:
        return _native_bool_to_boolean_object(node.value)
    elif type(node) is ast.PrefixExpression:
        right = evaluate(node.right)
        if _is_error(right):
            return right
        return _eval_prefix_expression(node.operator, right)
    elif type(node) is ast.InfixExpression:
        left = evaluate(node.left)
        if _is_error(left):
            return left

        right = evaluate(node.right)
        if _is_error(right):
            return right

        return _eval_infix_expression(node.operator, left, right)
    elif type(node) is ast.IfExpression:
        return _eval_if_expression(node)
    else:
        return None


def _eval_program(program: ast.Program) -> Object:
    result: Object

    for statement in program.statements:
        result = evaluate(statement)

        if isinstance(result, ReturnValue):
            return result.value
        elif isinstance(result, Error):
            return result

    return result


def _eval_block_statement(block: ast.BlockStatement) -> Object:
    result: Object

    for statement in block.statements:
        result = evaluate(statement)

        if result.object_type() == ObjectType.RETURN_VALUE or result.object_type() == ObjectType.ERROR:
            return result

    return result


def _eval_statements(statements: typing.List[ast.Statement]) -> Object:
    result = None

    for statement in statements:
        result = evaluate(statement)

        if isinstance(result, ReturnValue):
            return result

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
        return Error(f"unknown operator: -{right.object_type()}")

    value = right.value
    return Integer(-value)


def _eval_infix_expression(operator: str, left: Object, right: Object) -> Object:
    if left.object_type() == ObjectType.INTEGER and right.object_type() == ObjectType.INTEGER:
        return _eval_integer_infix_expression(operator, left, right)
    elif operator == '==':
        return _native_bool_to_boolean_object(left == right)
    elif operator == '!=':
        return _native_bool_to_boolean_object(left != right)
    elif left.object_type() != right.object_type():
        return Error(f"type mismatch: {left.object_type()} {operator} {right.object_type()}")
    else:
        return Error(f"unknown operator: {left.object_type()} {operator} {right.object_type()}")


def _eval_integer_infix_expression(operator: str, left: Object, right: Object) -> Object:
    if operator == '+':
        return Integer(left.value + right.value)
    elif operator == '-':
        return Integer(left.value - right.value)
    elif operator == '*':
        return Integer(left.value * right.value)
    elif operator == '/':
        return Integer(left.value / right.value)
    elif operator == '<':
        return _native_bool_to_boolean_object(left.value < right.value)
    elif operator == '>':
        return _native_bool_to_boolean_object(left.value > right.value)
    elif operator == '==':
        return _native_bool_to_boolean_object(left.value == right.value)
    elif operator == '!=':
        return _native_bool_to_boolean_object(left.value != right.value)
    else:
        return Error(f"unknown operator: {left.object_type()} {operator} {right.object_type()}")


def _eval_if_expression(if_expression: ast.IfExpression) -> Object:
    condition = evaluate(if_expression.condition)
    if _is_error(condition):
        return condition

    if _is_truthy(condition):
        return evaluate(if_expression.consequence)
    elif hasattr(if_expression, "alternative") and if_expression.alternative != None:
        return evaluate(if_expression.alternative)
    else:
        return NULL


def _is_truthy(obj: Object) -> bool:
    if obj == NULL:
        return False
    elif obj == TRUE:
        return True
    elif obj == FALSE:
        return False
    else:
        return True


def _is_error(obj: Object) -> bool:
    if obj:
        return obj.object_type() == Error
    return False
