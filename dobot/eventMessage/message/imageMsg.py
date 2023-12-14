from dobot.const import MessageType
from dobot.eventMessage.message.baseMsg import BaseMsg
from dobot.eventMessage.message.context import Context


class ImageMsg(BaseMsg):
    _MESSAGE_TYPE = MessageType.IMAGE.value
    _ctx: Context

    def __init__(self, **kwargs):
        super().__init__()
        self._url = kwargs.get('url', '')
        self._width = kwargs.get('width', 0)
        self._height = kwargs.get('height', 0)
        self._is_original = kwargs.get('isOriginal', 1)

    def dict(self):
        return {
            "url": self._url,
            "width": self._width,
            "height": self._height,
            "isOriginal": self._is_original
        }

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
