from dobot.const import MessageType
from dobot.eventMessage.message.baseMsg import BaseMsg
from dobot.eventMessage.message.context import Context


class ShareMsg(BaseMsg):
    _MESSAGE_TYPE = MessageType.SHARE.value
    _ctx: Context

    def __init__(self, message_body: dict):
        super().__init__()
        self._jump_url = message_body.get('jumpUrl', '')

    @property
    def jump_url(self):
        return self._jump_url
