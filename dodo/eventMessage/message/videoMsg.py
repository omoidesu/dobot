from dodo.const import MessageType
from dodo.eventMessage.message.baseMsg import BaseMsg
from dodo.eventMessage.message.context import Context


class VideoMsg(BaseMsg):
    _MESSAGE_TYPE = MessageType.VIDEO.value
    _ctx: Context

    def __init__(self, message_body: dict):
        self._url = message_body.get('url', '')
        self._cover_url = message_body.get('coverUrl', '')
        self._duration = message_body.get('duration', 0)
        self._size = message_body.get('size', 0)

    @property
    def url(self):
        return self._url

    @property
    def cover_url(self):
        return self._cover_url

    @property
    def duration(self):
        return self._duration

    @property
    def size(self):
        return self._size
