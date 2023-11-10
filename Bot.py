from BotClient import BotClient

from interface.AsyncRegisterObject import AsyncRegisterObject


class Bot(AsyncRegisterObject):
    def __init__(self, bot_id: str, bot_token: str):
        self.__ws = BotClient(bot_id, bot_token)

    def run(self):
        return self.__ws.run()


if __name__ == "__main__":
    bot = Bot("83199120", "ODMxOTkxMjA.77-9LAnvv70.4-jInox-uI8LTujPQZASLRGcxd_mn5twL-55m0LK7xc")
    bot.run()
