from typing import Union

from dobot.client import Client
from dobot.const import MessageType
from dobot.eventMessage.message.context import Context
from dobot.interface.BaseMsgInterface import BaseMsgInterface


class BaseMsg(BaseMsgInterface):
    _ctx: Context
    _client: Client

    def __init__(self):
        self._client = Client()

    async def send(self, content: Union[str, BaseMsgInterface]) -> dict:
        if isinstance(content, str):
            _message_type = MessageType.TEXT.value
            _message_body = {
                "content": content
            }
        else:
            _message_type = content._MESSAGE_TYPE
            _message_body = content.dict()

        kwargs = {
            'channelId': self.ctx.channel.id,
            'messageType': _message_type,
            'messageBody': _message_body
        }

        return await self._client.send_public_message(**kwargs)