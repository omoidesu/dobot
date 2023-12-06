from dobot.const import MessageType
from dobot.eventMessage.message.baseMsg import BaseMsg
from dobot.eventMessage.message.component.content import Content
from dobot.eventMessage.message.context import Context


class CardMsg(BaseMsg):
    _MESSAGE_TYPE = MessageType.CARD.value
    _ctx: Context

    def __init__(self, message_body: dict):
        super().__init__()
        self._content = Content(message_body.get('content', ''))
        self._card = message_body.get('card', '')

    @property
    def content(self):
        return self._content

    @property
    def card(self):
        return self._card
