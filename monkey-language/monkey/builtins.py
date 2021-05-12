from monkey.object import Builtin, Integer, String, Array, Error


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


BUILTINS = {
    "len": Builtin(len_builtin),
}
