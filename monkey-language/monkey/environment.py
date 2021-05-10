from monkey.object import Object


class Environment():
    def __init__(self) -> None:
        self.store = {}

    def get_variable(self, name: str):
        return self.store.get(name, None)

    def set_variable(self, name: str, value: Object):
        self.store[name] = value
        return value
