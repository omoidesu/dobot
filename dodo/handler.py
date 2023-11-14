from dodo.const import EventType
from dodo.interface.message import Message
from dodo.message.body import parse_message_body
from dodo.message.publicMessage import PublicMessage


class EventHandler:
    _prefix: str
    _handler_map: dict

    def __init__(self, prefix: str = '.'):
        self._prefix = prefix
        self._handler_map = {}

    def _reset_prefix(self, prefix: str):
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
        if _event_type == EventType.CHANNEL_MESSAGE:
            _msg = PublicMessage(_event_body)
            self._handle_cmd_msg(_msg)
        else:
            pass

    def _handle_cmd_msg(self, msg: Message):
        pass

    def _handle_event_msg(self, msg: Message):
        pass

    def _filter_msg_cmd(self, cmd_with_prefix: str):
        awaitable_func = self._handler_map.get(cmd_with_prefix, False)
        if not awaitable_func:
            raise Exception("Dont fetch cmd")
        return awaitable_func

    def _register_msg_event(self, cmd: str, prefix_ls: set[str], func):
        _msg_command_dict = self._handler_map.get("msg", {})
        for item in prefix_ls:
            _msg_command_dict[item + cmd] = func
        self._handler_map["msg"] = _msg_command_dict
