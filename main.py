from bot import VKBot


try:
    bot = VKBot()
    bot.run()
except Exception as e0:
    print(e0)
