import asyncio

from dodo.const import EventType
from dodo.interface.message import Message
from dodo.log import MyLogger
from dodo.message.publicMessage import PublicMessage

logger = MyLogger()

class EventHandler:
    _prefix: str
    _handler_map: dict

    def __init__(self, prefix: str = '.'):
        self._prefix = prefix
        self._handler_map = {}

    def _reset_prefix(self, prefix: str):
        """
        设置全局的指令前缀
        :param prefix: 触发指令前缀
        :return:
        """
        if prefix is not None:
            self._prefix = prefix
        else:
            self._prefix = '.'

    def _handle_msg(self, msg_dict: dict):
        """
        将ws返回参数解析成对应Event的Msg
        :param msg_dict: ws返回的解析后的msg
        :return: Msg实体
        """
        _data = msg_dict.get("data", {})
        _event_body = _data.get("eventBody", None)
        _event_type = _data.get("eventType", None)
        if _event_type == EventType.CHANNEL_MESSAGE.value:
            _msg = PublicMessage(_event_body)
            self._handle_cmd_msg(_msg)
        else:
            pass

    def _handle_cmd_msg(self, msg: Message):
        """
        处理消息事件的方法
        :param msg: ws返回的msg实体信息
        :return: 被调度方法
        """
        try:
            awaitable_func = self._filter_msg_cmd(msg)
            return asyncio.gather(awaitable_func(msg))
        except Exception as e:
            logger.debug(e)

    def _handle_event_msg(self, msg: Message):
        """
        处理非消息事件的方法
        :param msg: ws返回的msg实体信息
        :return: 被调度方法
        """
        pass

    def _filter_msg_cmd(self, msg: Message) -> asyncio.coroutine:
        """
        消息类型的msg过滤器，返回被调度的方法
        :param msg: ws返回的msg实体信息
        :return: 被调度方法
        """
        _msg_content_ls = msg.body.content.split(" ")
        if len(_msg_content_ls) > 0:
            _cmd_with_prefix = _msg_content_ls[0]
            awaitable_func = self._handler_map.get("msg", {}).get(_cmd_with_prefix, False)
            if not awaitable_func:
                raise Exception("Dont fetch cmd")
            return awaitable_func

    def _register_msg_event(self, cmd: str, prefix_ls: set, func):
        """
        注册命令至handler中等待调度
        :param cmd: 指令触发字符串
        :param prefix_ls: 前缀列表
        :param func: 被调度函数
        :return:
        """
        _msg_command_dict = self._handler_map.get("msg", {})
        if len(prefix_ls) == 0:
            prefix_ls = {self._prefix}
        for item in prefix_ls:
            _msg_command_dict[item + cmd] = func
        self._handler_map["msg"] = _msg_command_dict
