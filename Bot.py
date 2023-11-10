from BotClient import BotClient

from interface.AsyncRegisterObject import AsyncRegisterObject


class Bot(AsyncRegisterObject):
    def __init__(self, bot_id: str, bot_token: str):
        self.__ws = BotClient(bot_id, bot_token)

    def run(self):
        return self.__ws.run()
