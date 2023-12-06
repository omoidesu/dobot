from typing import Union
import warnings

from dobot.cert import AuthInfo
from dobot.client import Client
from dobot.const import Route, EventType
from dobot.eventMessage.msg import Msg
from dobot.exception import ApiRequestError, RequestError
from dobot.handler import EventHandler
from dobot.interface.AsyncRegisterObject import AsyncRegisterObject
from dobot.websocket import BotClient


class Bot(AsyncRegisterObject):
    """
    Bot 核心类
    """
    __ws: BotClient
    __handler: EventHandler
    client: Client

    def __init__(self, bot_id: str, bot_token: str, time_log: bool = False):
        AuthInfo(bot_id, bot_token)
        self.__handler = EventHandler()
        self.__ws = BotClient(self.__handler)
        self.client = Client(time_log)

    def prefix(self, prefix: str = None):
        """
        设置全局通用的指令前缀
        :param prefix: 指令前缀
        :return: None
        """
        self.__handler.reset_prefix(prefix)

    def on_message(self,
                   cmd: str,
                   prefix: Union[list, tuple] = (),
                   at_bot: bool = False):
        """
        消息事件的装饰器方法，用于处理消息类的业务
        :param cmd: 触发指令
        :param prefix: 指令前缀
        :param at_bot: 是否@bot才能使用
        :return: 被装饰方法的返回值
        """

        def decorator(func):
            async def wrapper(msg: Msg, *args, **kwargs):
                res = await func(msg, *args, **kwargs)
                return res

            self.__handler.register_msg_event(cmd, set(prefix), at_bot, wrapper)
            return wrapper

        return decorator

    def on_event(self, event_type: EventType):
        """
        其余事件的装饰器方法，用于处理服务器事件的业务
        :param event_type: 事件的类型
        """

        def decorator(func):
            async def wrapper(msg: Msg, *args, **kwargs):
                res = await func(msg, *args, **kwargs)
                return res

            self.__handler.register_event(event_type, wrapper)
            return wrapper

        return decorator

    def on_reaction(self,
                    island_id_list: Union[list, tuple] = ("*",),
                    channel_id_list: Union[list, tuple] = ("*",),
                    emoji_list: list = ("*",),
                    reaction_type: int = None):
        """
        消息事件的装饰器方法，用于处理表情反应类的业务
        :param island_id_list: 群ID列表
        :param channel_id_list: 频道ID列表
        :param emoji_list: emoji列表
        :param reaction_type: 反应类型（0-删除 1-新增）
        :return:
        """
        warnings.warn("这个方法暂时被废弃，归并到on_event中", DeprecationWarning)

        def decorator(func):
            async def wrapper(msg: Msg, *args, **kwargs):
                res = await func(msg, *args, **kwargs)
                return res

            self.__handler.register_reaction_event(set(island_id_list), set(channel_id_list), set(emoji_list), reaction_type)
            return wrapper

        return decorator

    def run(self):
        import requests

        response = requests.post(Route.GET_BOT_INFO.value, headers=AuthInfo.get_instance().header)
        if response.status_code != 200:
            raise RequestError(response.status_code, Route.GET_BOT_INFO.value)

        response_json = response.json()
        status = response_json.get("status", -9999)
        if status != 0:
            raise ApiRequestError(response.status_code, Route.GET_BOT_INFO.value, {}, status,
                                  response_json.get("message", ""))

        AuthInfo.get_instance().me = response_json.get("data", {}).get("dodoSourceId")

        return self.__ws.run()
