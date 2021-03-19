import json
import sys
import logging

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import getrandbits
from command_system import command_list
import messageHandler


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

                if event.type == VkEventType.MESSAGE_NEW:

                            message, attachment = messageHandler.create_answer(event)
                            if message is not None or attachment is not None:
                                if event.from_chat:
                                    self.replyToChat(event.chat_id, message, attachment)
                                elif event.from_user:
                                    self.replyToUser(event.user_id, message, attachment)

        except KeyboardInterrupt:
            self.logger.info("Bot finished.")
            sys.exit("\nExit")

    def replyToChat(self, chat_id: int, msg: str, attach: str) -> None:
        """Ответ от бота в чат"""
        self.logger.info(f'Chat: {chat_id} Message: {msg} Attachment: {attach}')
        self.session.method('messages.send', {
            "chat_id": chat_id,
            "message": msg,
            "attachment": attach,
            "random_id": getrandbits(64)
        })
    def replyToUser(self, user_id: int, msg: str, attach: str) -> None:
        """Ответ от бота в чат"""
        self.logger.info(f'User: {user_id} Message: {msg} Attachment: {attach}')
        self.session.method('messages.send', {
            "user_id": user_id,
            "message": msg,
            "attachment": attach,
            "random_id": getrandbits(64)
        })

