import json
import sys

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import getrandbits

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from extensions.commands import Command
from classes.logger import Logger


class VKBot:

    def __init__(self):

        with open("config.json", 'r') as f:
            self.config = json.load(f)

        self.logger = Logger(self.__class__.__name__, self.config['level'], self.config['write_file'])
        self.session = vk_api.VkApi(token=self.config["token"])

    def run(self) -> None:
        """Запуск проверки ивентов"""

        self.logger.info("Bot launched...")
        longpoll = VkBotLongPoll(self.session, self.config['public_id'])
        command = Command({})

        try:
            for event in longpoll.listen():

                if event.type == VkBotEventType.MESSAGE_NEW and (event.from_chat or event.from_user):

                    e_msg = event.object.message
                    msg = e_msg['text'].lower()
                    username = self.get_username(e_msg['from_id'])
                    _vars = {
                        "user_id": e_msg['from_id'],
                        "username": username,
                    }
                    command.values = _vars
                    answer = command.command(msg)
                    if answer:
                         self.reply(event.chat_id, answer, None)

        except KeyboardInterrupt:
            self.logger.info("Bot finished.")
            sys.exit("\nExit")

    def reply(self, chat_id: int, msg: str, attach: str) -> None:
        """Ответ от бота в чат"""

        self.session.method('messages.send', {
            "chat_id": chat_id,
            "message": msg,
            "attachment": attach,
            "random_id": getrandbits(64)
        })

    def get_username(self, user_id: int) -> str:
         """Получить имя пользователя """

         return self.session.method("users.get", {"user_ids": user_id})[0]['first_name']

