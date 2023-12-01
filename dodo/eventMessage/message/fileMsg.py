from dodo.const import MessageType
from dodo.eventMessage.message.baseMsg import BaseMsg
from dodo.eventMessage.message.context import Context


class FileMsg(BaseMsg):
    _MESSAGE_TYPE = MessageType.FILE.value
    _ctx: Context
    def __init__(self, message_body: dict):
        self._url = message_body.get('url', '')
        self._name = message_body.get('name', '')
        self._size = message_body.get('size', 0)

    @property
    def url(self):
        return self._url

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size