from dodo.const import MessageType
from dodo.eventMessage.message.baseMsg import BaseMsg
from dodo.eventMessage.message.context import Context


class ImageMsg(BaseMsg):
    _MESSAGE_TYPE = MessageType.IMAGE.value
    _ctx: Context

    def __init__(self, message_body: dict):
        self._url = message_body.get('url', '')
        self._width = message_body.get('width', 0)
        self._height = message_body.get('height', 0)
        self._is_original = message_body.get('isOriginal', 0)

    @property
    def url(self):
        return self._url

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def is_original(self):
        return self._is_original
