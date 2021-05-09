import enum


class ObjectType(enum.Enum):
    INTEGER = "INTEGER"


class Object:
    def object_type(self) -> ObjectType:
        raise NotImplementedError()

    def inspect(self) -> str:
        raise NotImplementedError()


class Integer:
    def __init__(self, value: int) -> None:
        self.value = value

    def object_type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return str(self.value)
