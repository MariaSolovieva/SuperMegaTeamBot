from .actions.currency import get_rate
from .action import ActionFunc, ActionText


class Command:

    list_of_commands = [
        ActionText(['привет, бот', 'бот, привет', 'привет бот', 'бот привет'], "Приветствую, @id{user_id}({username})"),
        ActionFunc(['текущий курс'], get_rate)
    ]


    def __init__(self, values: dict):
        """
        values: Аргументы для вставки в текст, такие как id юзера и его ник
        """

        self.values = values

    def command(self, key: str) -> bool:
        """Проверяем есть ли такая команда у бота"""

        cmd = next((
                command for command in self.list_of_commands if key in command.keys
                ), None)
        if cmd:
            return cmd().format(**self.values)

