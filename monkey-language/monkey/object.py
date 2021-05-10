import enum


class ObjectType(enum.Enum):
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"
    RETURN_VALUE = "RETURN_VALUE"


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
