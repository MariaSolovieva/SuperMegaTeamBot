import json
import vk_api
import commands
from command_system import command_list

def get_username(session, user_id: int) -> str:
    """Получить имя пользователя """

    return session.method("users.get", {"user_ids": user_id})[0]['first_name']

def connect():
    with open("config.json", 'r') as f:
        config = json.load(f)
    session = vk_api.VkApi(token=config["token"])
    f.close()
    return session


def create_answer(data):
   body = data.text.lower()
   message = None
   attachment = None
   for c in command_list:
        if body in c.keys:
            message, attachment = c.process()
            if '{user_id}' in message:
                api = connect()
                first_name = get_username(api, data.user_id)
                message = message.format(user_id = data.user_id, username = first_name)

   return message, attachment