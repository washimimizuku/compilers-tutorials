import typing
import monkey.ast as ast
from monkey.builtins import BUILTINS
from monkey.environment import Environment, new_enclosed_environment
from monkey.object import (
    Object, ObjectType, Hashable,
    Integer, Boolean, String, Null, Array, HashPair, Hash,
    ReturnValue, Error, Function, Builtin
)

TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()


def evaluate(node: ast.Node, env: Environment) -> Object:
    # Statements
    if type(node) is ast.Program:
        return _eval_program(node, env)
    elif type(node) is ast.ExpressionStatement:
        return evaluate(node.expression, env)
    elif type(node) is ast.BlockStatement:
        return _eval_block_statement(node, env)
    elif type(node) is ast.ReturnStatement:
        value = evaluate(node.return_value, env)

        if _is_error(value):
            return value
        return ReturnValue(value)
    elif type(node) is ast.LetStatement:
        value = evaluate(node.value, env)
        if _is_error(value):
            return value
        env.set_variable(node.name.value, value)

    elif type(node) is ast.Identifier:
        return _eval_identifier(node, env)

    # Expressions
    elif type(node) is ast.IntegerLiteral:
        return Integer(node.value)
    elif type(node) is ast.BooleanLiteral:
        return _native_bool_to_boolean_object(node.value)
    elif type(node) is ast.StringLiteral:
        return String(node.value)
    elif type(node) is ast.PrefixExpression:
        right = evaluate(node.right, env)
        if _is_error(right):
            return right
        return _eval_prefix_expression(node.operator, right)
    elif type(node) is ast.InfixExpression:
        left = evaluate(node.left, env)
        if _is_error(left):
            return left

        right = evaluate(node.right, env)
        if _is_error(right):
            return right

        return _eval_infix_expression(node.operator, left, right)
    elif type(node) is ast.IfExpression:
        return _eval_if_expression(node, env)
    elif type(node) is ast.FunctionLiteral:
        parameters = node.parameters
        body = node.body
        return Function(parameters, body, env)
    elif type(node) is ast.CallExpression:
        function = evaluate(node.function, env)
        if _is_error(function):
            return function
        arguments = _eval_expressions(node.arguments, env)
        if len(arguments) == 1 and _is_error(arguments[0]):
            return arguments[0]
        return _apply_function(function, arguments)
    elif type(node) is ast.ArrayLiteral:
        elements = _eval_expressions(node.elements, env)
        if len(elements) == 1 and _is_error(elements[0]):
            return elements[0]
        return Array(elements)
    elif type(node) is ast.HashLiteral:
        return _eval_hash_literal(node, env)
    elif type(node) is ast.IndexExpression:
        left = evaluate(node.left, env)
        if _is_error(left):
            return left
        index = evaluate(node.index, env)
        if _is_error(index):
            return index
        return _eval_index_expression(left, index)
    else:
        return None


def _apply_function(function: Object, arguments: typing.List[Object]) -> Object:
    if isinstance(function, Function):
        extended_env = _extended_function_env(function, arguments)
        evaluated = evaluate(function.body, extended_env)
        return _unwrap_return_value(evaluated)

    elif isinstance(function, Builtin):
        return function.function(arguments)

    else:
        return Error(f"not a function: {function.object_type()}")


def _extended_function_env(function: Function, arguments: typing.List[Object]) -> Environment:
    env = new_enclosed_environment(function.env)

    for index in range(len(function.parameters)):
        env.set_variable(function.parameters[index].value, arguments[index])

    return env


def _unwrap_return_value(obj: Object) -> Object:
    if isinstance(obj, ReturnValue):
        return obj.value
    return obj


def _eval_program(program: ast.Program, env: Environment) -> Object:
    result: Object

    for statement in program.statements:
        result = evaluate(statement, env)

        if isinstance(result, ReturnValue):
            return result.value
        elif isinstance(result, Error):
            return result

    return result


def _eval_block_statement(block: ast.BlockStatement, env: Environment) -> Object:
    result: Object

    for statement in block.statements:
        result = evaluate(statement, env)

        if result.object_type() == ObjectType.RETURN_VALUE or result.object_type() == ObjectType.ERROR:
            return result

    return result


def _eval_statements(statements: typing.List[ast.Statement], env: Environment) -> Object:
    result = None

    for statement in statements:
        result = evaluate(statement, env)

        if isinstance(result, ReturnValue):
            return result

    return result


def _eval_expressions(expressions: typing.List[ast.Expression], env: Environment) -> Object:
    result: typing.List[Object] = []

    for expression in expressions:
        evaluated = evaluate(expression, env)
        if evaluated is None:
            return evaluated

        if _is_error(evaluated):
            return evaluated

        result.append(evaluated)

    return result


def _native_bool_to_boolean_object(input: bool) -> Boolean:
    if input:
        return TRUE
    else:
        return FALSE


def _eval_identifier(node: ast.Identifier, env: Environment) -> Object:
    value = env.get_variable(node.value)
    if value is not None:
        return value

    value = BUILTINS.get(node.value, None)
    if value is not None:
        return value

    return Error(f"identifier not found: {node.value}")


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
    if left.object_type() == ObjectType.STRING and right.object_type() == ObjectType.STRING:
        return _eval_string_infix_expression(operator, left, right)
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


def _eval_string_infix_expression(operator: str, left: Object, right: Object) -> Object:
    if operator == '+':
        return String(left.value + right.value)
    else:
        return Error(f"unknown operator: {left.object_type()} {operator} {right.object_type()}")


def _eval_if_expression(if_expression: ast.IfExpression, env: Environment) -> Object:
    condition = evaluate(if_expression.condition, env)
    if _is_error(condition):
        return condition

    if _is_truthy(condition):
        return evaluate(if_expression.consequence, env)
    elif hasattr(if_expression, "alternative") and if_expression.alternative != None:
        return evaluate(if_expression.alternative, env)
    else:
        return NULL


def _eval_index_expression(left: Object, index: Object) -> Object:
    if left.object_type() == ObjectType.ARRAY and index.object_type() == ObjectType.INTEGER:
        return _eval_array_index_expression(left, index)
    elif left.object_type() == ObjectType.HASH:
        return _eval_hash_index_expression(left, index)
    else:
        return Error(f"index operator not supported: {left.object_type()}")


def _eval_array_index_expression(array: Object, index: Object) -> Object:
    array_object = array
    idx = index.value
    maximum = len(array_object.elements) - 1

    if idx < 0 or idx > maximum:
        return NULL

    return array_object.elements[idx]


def _eval_hash_index_expression(hash_object: Object, index: Object) -> Object:
    if not isinstance(index, Hashable):
        return Error(f"unusable as hash key: {index.object_type()}")

    pair = hash_object.pairs.get(index.hash_key(), None)
    if pair is None:
        return NULL

    return pair.value


def _eval_hash_literal(node: ast.HashLiteral, env: Environment) -> Object:
    pairs = {}

    for node_key, node_value in node.pairs.items():
        key = evaluate(node_key, env)
        if _is_error(key) or key is None:
            return key

        if not isinstance(key, Hashable):
            return Error(f"unusable as hash key: {key.type}")

        value = evaluate(node_value, env)
        if _is_error(value) or value is None:
            return value

        hashed = key.hash_key()
        pairs[hashed] = HashPair(key, value)

    return Hash(pairs)


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
