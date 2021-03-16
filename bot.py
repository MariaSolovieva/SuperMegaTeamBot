import json
import sys
import logging

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from commands import commands


class VKBot:

    def __init__(self):

        with open("config.json", 'r') as f:
            self.config = json.load(f)

        level = getattr(logging, self.config['level'])
        write_file = self.config["write_file"]
        logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.__class__.__name__)
        if write_file:
            file_log = logging.FileHandler("{}.log".format(self.__class__.__name__))
            file_log.setLevel(level)
            format_log = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_log.setFormatter(format_log)
            self.logger.addHandler(file_log)

        self.session = vk_api.VkApi(token=self.config["token"])

    def run(self) -> None:
        """Запуск проверки ивентов"""

        self.logger.info("Bot launched...")

        longpoll = VkLongPoll(self.session)

        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.from_chat:
                    msg = event.text.lower()
                    if msg in commands:
                        username = self.get_username(event.user_id)
                        self.reply(event.chat_id, commands[msg].format(user_id=event.user_id, username=username))
        except KeyboardInterrupt:
            self.logger.info("Bot finished.")
            sys.exit("\nExit")

    def get_username(self, user_id: int) -> str:
        """Получить имя пользователя """

        return self.session.method("users.get", {"user_ids": user_id})[0]['first_name']

    def reply(self, chat_id: int, msg: str) -> None:
        """Ответ от бота в чат"""

        self.session.method('messages.send', {
            "chat_id": chat_id,
            "message": msg,
            "random_id": 0
        })

