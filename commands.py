import command_system


"""Приветствие"""
def hello():
   message = 'Приветствую, @id{user_id}({username})'
   return message, ''

hello_command = command_system.Command()

hello_command.keys = ['привет, бот', 'бот, привет', 'привет бот', 'бот привет']
hello_command.description = 'Поприветствую тебя'
hello_command.process = hello