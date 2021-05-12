import enum
import typing

from monkey.ast import Identifier, Expression, BlockStatement


class ObjectType(enum.Enum):
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    STRING = "STRING"
    NULL = "NULL"
    RETURN_VALUE = "RETURN_VALUE"
    ERROR = "ERROR"
    FUNCTION = "FUNCTION"
    BUILTIN = "BUILTIN"
    ARRAY = "ARRAY"


class Object:
    def object_type(self) -> ObjectType:
        raise NotImplementedError()

    def inspect(self) -> str:
        raise NotImplementedError()


class Integer:
    def __init__(self, value: int) -> None:
        self.value: int = value

    def object_type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return str(self.value)


class Boolean:
    def __init__(self, value: bool) -> None:
        self.value: bool = value

    def object_type(self) -> ObjectType:
        return ObjectType.BOOLEAN

    def inspect(self) -> str:
        return str(self.value).lower()


class String:
    def __init__(self, value: str) -> None:
        self.value: str = value

    def object_type(self) -> ObjectType:
        return ObjectType.STRING

    def inspect(self) -> str:
        return self.value


class Null:
    def __init__(self) -> None:
        self.value = None

    def object_type(self) -> ObjectType:
        return ObjectType.NULL

    def inspect(self) -> str:
        return str(self.value)


class ReturnValue:
    def __init__(self, value: Object) -> None:
        self.value: Object = value

    def object_type(self) -> ObjectType:
        return ObjectType.RETURN_VALUE

    def inspect(self) -> str:
        return self.value.inspect()


class Error:
    def __init__(self, message: str) -> None:
        self.message: str = message

    def object_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return f"ERROR: {self.message}"


class Function(Expression):
    def __init__(self, parameters, body, env) -> None:
        self.parameters: typing.List[Identifier] = parameters
        self.body: BlockStatement = body
        self.env = env

    def object_type(self) -> ObjectType:
        return ObjectType.FUNCTION

    def inspect(self) -> str:
        parameters: typing.List[str] = []
        for parameter in self.parameters:
            parameters.append(str(parameter))

        message = f"fn({', '.join(parameters)})"
        message += "{\n"
        message += str(self.body)
        message += "\n}"

        return message


class Builtin(Object):
    def __init__(self, function) -> None:
        self.function = function

    def object_type(self) -> ObjectType:
        return ObjectType.BUILTIN

    def inspect(self) -> str:
        return "builtin function"


class Array(Object):
    def __init__(self, elements) -> None:
        self.elements = elements

    def object_type(self) -> ObjectType:
        return ObjectType.ARRAY

    def inspect(self) -> str:
        elements = []
        for element in self.elements:
            elements.append(element.inspect())

        return f"[{', '.join(elements)}]"
