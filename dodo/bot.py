from dodo.client import Client
from .cert import AuthCell
from .interface.AsyncRegisterObject import AsyncRegisterObject
from .websocket import BotClient


class Bot(AsyncRegisterObject):
    """
    Bot 核心类
    """
    __ws: BotClient
    client: Client

    def __init__(self, bot_id: str, bot_token: str, log_time: bool = False):
        AuthCell(bot_id, bot_token)
        self.__ws = BotClient()
        self.client = Client(log_time)

    def run(self):
        return self.__ws.run()


if __name__ == '__main__':
    bot = Bot("83199120", "ODMxOTkxMjA.77-9LAnvv70.4-jInox-uI8LTujPQZASLRGcxd_mn5twL-55m0LK7xc")
    bot.run()
