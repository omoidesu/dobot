from dodo.const import MessageType
from dodo.eventMessage.message.baseMsg import BaseMsg
from dodo.eventMessage.message.component.content import Content
from dodo.eventMessage.message.context import Context


class CardMsg(BaseMsg):
    _MESSAGE_TYPE = MessageType.CARD.value
    _ctx: Context

    def __init__(self, message_body: dict):
        self._content = Content(message_body.get('content', ''))
        self._card = message_body.get('card', '')

    @property
    def content(self):
        return self._content

    @property
    def card(self):
        return self._card
