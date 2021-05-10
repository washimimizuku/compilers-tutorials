from monkey.object import Object


class Environment():
    def __init__(self) -> None:
        self.store = {}
        self.outer: Environment = None

    def get_variable(self, name: str):
        obj = self.store.get(name, None)
        if obj is None and self.outer != None:
            obj = self.outer.store.get(name, None)
        return obj

    def set_variable(self, name: str, value: Object):
        self.store[name] = value
        return value


def new_enclosed_environment(outer: Environment) -> Environment:
    env = Environment()
    env.outer = outer
    return env
