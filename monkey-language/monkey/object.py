import enum
import hashlib
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
    HASH = "HASH"


class Object:
    def object_type(self) -> ObjectType:
        raise NotImplementedError()

    def inspect(self) -> str:
        raise NotImplementedError()


class HashKey:
    def __init__(self, type: ObjectType, value: int):
        self.type = type
        self.value = value

    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, HashKey) and other.type == self.type and other.value == self.value:
            return True

        return False

    def __ne__(self, other: typing.Any) -> bool:
        if isinstance(other, HashKey) and other.type == self.type and other.value == self.value:
            return False

        return True

    def __hash__(self) -> int:
        return hash(f"{self.type}-{self.value}")


class Hashable:
    def hash_key(self) -> HashKey:
        raise NotImplementedError()


class Integer(Object, Hashable):
    def __init__(self, value: int) -> None:
        self.value: int = value

    def object_type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return str(self.value)

    def hash_key(self) -> HashKey:
        return HashKey(self.object_type(), self.value)


class Boolean(Object, Hashable):
    def __init__(self, value: bool) -> None:
        self.value: bool = value

    def object_type(self) -> ObjectType:
        return ObjectType.BOOLEAN

    def inspect(self) -> str:
        return str(self.value).lower()

    def hash_key(self) -> HashKey:
        value = 0  # False
        if self.value:
            value = 1  # True

        return HashKey(self.object_type(), value)


class String(Object, Hashable):
    def __init__(self, value: str) -> None:
        self.value: str = value

    def object_type(self) -> ObjectType:
        return ObjectType.STRING

    def inspect(self) -> str:
        return self.value

    def hash_key(self) -> HashKey:
        return HashKey(self.object_type(), hashlib.sha256(self.value.encode()).hexdigest())


class Null(Object):
    def __init__(self) -> None:
        self.value = None

    def object_type(self) -> ObjectType:
        return ObjectType.NULL

    def inspect(self) -> str:
        return str(self.value)


class ReturnValue(Object):
    def __init__(self, value: Object) -> None:
        self.value: Object = value

    def object_type(self) -> ObjectType:
        return ObjectType.RETURN_VALUE

    def inspect(self) -> str:
        return self.value.inspect()


class Error(Object):
    def __init__(self, message: str) -> None:
        self.message: str = message

    def object_type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return f"ERROR: {self.message}"


class Function(Object):
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


class HashPair:
    def __init__(self, key: Object, value: Object) -> None:
        self.key = key
        self.value = value


class Hash(Object):
    def __init__(self, pairs: typing.Dict[HashKey, HashPair]) -> None:
        self.pairs = pairs

    def object_type(self) -> ObjectType:
        return ObjectType.HASH

    def inspect(self) -> str:
        pairs = []
        for pair in self.pairs:
            pairs.append(f"{pair.key.inspect()}: {pair.value.inspect()}")

        return f"[{', '.join(pairs)}]"
