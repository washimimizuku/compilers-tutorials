from monkey.object import Builtin, Integer, String, Error


def len_function(args):
    if len(args) != 1:
        return Error(f"wrong number of arguments. got={len(args)}, want=1")

    string = args[0]
    if isinstance(string, String):
        return Integer(len(string.value))
    else:
        return Error(f"argument to 'len' not supported, got={string.object_type()}")


BUILTINS = {
    "len": Builtin(len_function),
}
