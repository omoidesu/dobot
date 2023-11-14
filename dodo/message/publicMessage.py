from typing import Union

from dodo import Bot
from dodo.client import Client
from dodo.const import MessageType
from dodo.exception.typeError import MessageTypeError
from dodo.interface.message import Message
from dodo.message.body import MessageBody, TextMessage, parse_message_body
from dodo.message.context import Context


class PublicMessage(Message):
    def __init__(self, event_body: dict):
        self._client = Client()
        self.msg_id = event_body.get("messageId", '')
        self.msg_type = event_body.get('messageType', '')
        # self.ctx = ctx
        _body = parse_message_body(event_body["messageType"], event_body)
        self.body = _body

    async def reply(self, content: Union[str, MessageBody]):
        if isinstance(content, str):
            content = TextMessage(content)

        kwargs = {
            'channelId': self.ctx.channel.id,
            'messageType': content.message_type.value,
            'messageBody': str(content),
            'referencedMessageId': self.msg_id,
        }

        return await self._client.send_public_message(**kwargs)

    async def edit(self, content: Union[str, MessageBody]):
        if isinstance(content, str):
            content = TextMessage(content)

        if self.msg_type != content.message_type:
            raise MessageTypeError([], self.msg_type.value)

        kwargs = {
            'messageId': self.msg_id,
            'messageBody': str(content)
        }

        return await self._client.edit_public_message(**kwargs)

    async def delete(self, reason: str):
        kwargs = {'messageId': self.msg_id}
        if reason:
            kwargs['reason'] = reason

        return await self._client.delete_public_message(**kwargs)

    async def fetch_emoji_list(self):
        raise Exception("Public msg event dont have fetch_emoji_list method!")

    async def fetch_emoji_user(self, emoji: str):
        ...

    async def add_reaction(self, emoji: str):
        ...

    async def delete_reaction(self, emoji: str, user_id: str):
        ...
