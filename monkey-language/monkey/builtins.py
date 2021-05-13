from monkey.object import (
    Builtin, Integer, String, Array, Error, ObjectType, Null
)


def len_builtin(args):
    if len(args) != 1:
        return Error(f"wrong number of arguments. got={len(args)}, want=1")

    argument = args[0]
    if isinstance(argument, Array):
        return Integer(len(argument.elements))
    if isinstance(argument, String):
        return Integer(len(argument.value))
    else:
        return Error(f"argument to 'len' not supported, got={argument.object_type()}")


def first_builtin(args):
    if len(args) != 1:
        return Error(f"wrong number of arguments. got={len(args)}, want=1")

    array = args[0]
    if array.object_type() != ObjectType.ARRAY:
        return Error(f"argument to 'first' must be ObjectType.ARRAY, got {array.object_type()}")

    if len(array.elements) > 0:
        return array.elements[0]

    return Null()


def last_builtin(args):
    if len(args) != 1:
        return Error(f"wrong number of arguments. got={len(args)}, want=1")

    array = args[0]
    if array.object_type() != ObjectType.ARRAY:
        return Error(f"argument to 'last' must be ObjectType.ARRAY, got {array.object_type()}")

    if len(array.elements) > 0:
        return array.elements[-1]

    return Null()


def rest_builtin(args):
    if len(args) != 1:
        return Error(f"wrong number of arguments. got={len(args)}, want=1")

    array = args[0]
    if array.object_type() != ObjectType.ARRAY:
        return Error(f"argument to 'rest' must be ObjectType.ARRAY, got {array.object_type()}")

    if len(array.elements) > 0:
        rest_elements = array.elements[1:]
        return rest_elements

    return Null()


def push_builtin(args):
    if len(args) != 2:
        return Error(f"wrong number of arguments. got={len(args)}, want=2")

    array = args[0]
    new_element = args[1]

    if array.object_type() != ObjectType.ARRAY:
        return Error(f"argument to 'push' must be ObjectType.ARRAY, got {array.object_type()}")

    new_array = array.elements[:]
    new_array.append(new_element)

    return new_array


def puts_builtin(args):
    for arg in args:
        print(arg.inspect())

    return Null()


BUILTINS = {
    "len": Builtin(len_builtin),
    "first": Builtin(first_builtin),
    "last": Builtin(last_builtin),
    "rest": Builtin(rest_builtin),
    "push": Builtin(push_builtin),
    "puts": Builtin(puts_builtin),
}
