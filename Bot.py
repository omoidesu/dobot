from BotClient import BotClient
import logging


class Bot:
    def __init__(self, bot_id: str, bot_token: str):
        self.__ws = BotClient(bot_id, bot_token)


if __name__ == "__main__":
    bot = Bot("83199120", "ODMxOTkxMjA.77-9LAnvv70.4-jInox-uI8LTujPQZASLRGcxd_mn5twL-55m0LK7xc")
