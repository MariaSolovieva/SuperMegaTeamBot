from typing import Callable


class Action:

    def __init__(self, keys: list):
        self.keys = tuple(keys)


class ActionFunc(Action):
    """Экшен с вызовом функции"""

    def __init__(self, keys: list, func: Callable):

        super().__init__(keys)
        self.func = func

    def __call__(self):
        return self.func()


class ActionText(Action):
    """Экшен возвращающий текст"""

    def __init__(self, keys: list, text: str):

        super().__init__(keys)
        self.text = text

    def __call__(self):
        return self.text

