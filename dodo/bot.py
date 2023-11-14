from typing import Union

from dodo.cert import AuthInfo
from dodo.client import Client
from dodo.handler import EventHandler
from dodo.interface.AsyncRegisterObject import AsyncRegisterObject
from dodo.interface.message import Message
from dodo.websocket import BotClient


class Bot(AsyncRegisterObject):
    """
    Bot 核心类
    """
    __ws: BotClient
    __handler: EventHandler
    client: Client

    def __init__(self, bot_id: str, bot_token: str, log_time: bool = False):
        AuthInfo(bot_id, bot_token)
        self.__handler = EventHandler()
        self.__ws = BotClient(self.__handler)
        self.client = Client(log_time)

    def prefix(self, prefix: str = None):
        """
        设置全局通用的指令前缀
        :param prefix: 指令前缀
        :return: None
        """
        self.__handler._reset_prefix(prefix)

    def on_message(self, cmd: str, prefix: Union[list, tuple] = ()):
        """
        消息事件的装饰器方法，用于处理消息类的业务
        :param cmd: 触发指令
        :param prefix: 指令前缀
        :return: 被装饰方法的返回值
        """
        def decorator(func):
            async def wrapper(msg: Message, *args, **kwargs):
                res = await func(msg, *args, **kwargs)
                return res

            self.__handler._register_msg_event(cmd, set(prefix), wrapper)
            return wrapper

        return decorator


    def run(self):
        return self.__ws.run()


if __name__ == '__main__':
    bot = Bot("83199120", "ODMxOTkxMjA.77-9LAnvv70.4-jInox-uI8LTujPQZASLRGcxd_mn5twL-55m0LK7xc")
    bot.run()
