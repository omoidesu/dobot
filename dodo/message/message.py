from typing import Union

from dodo import Bot
from dodo.const import MessageType
from dodo.exception.typeError import MessageTypeError
from dodo.message.body import MessageBody, TextMessage
from dodo.message.context import Context


class Message:
    _bot: Bot
    msg_id: str
    msg_type: MessageType
    ctx: Context
    body: MessageBody

    async def reply(self, content: Union[str, MessageBody]):
        ...

    async def edit(self, content: Union[str, MessageBody]):
        ...

    async def delete(self, reason: str):
        ...

    async def fetch_emoji_list(self):
        ...

    async def fetch_emoji_user(self, emoji: str):
        ...

    async def add_reaction(self, emoji: str):
        ...

    async def delete_reaction(self, emoji: str, user_id: str):
        ...


class PublicMessage(Message):
    def __init__(self, bot: Bot, msg_id: str, msg_type: MessageType, ctx: Context, body: MessageBody):
        self._bot = bot
        self.msg_id = msg_id
        self.msg_type = msg_type
        self.ctx = ctx
        self.body = body

    async def reply(self, content: Union[str, MessageBody]):
        if isinstance(content, str):
            content = TextMessage(content)

        kwargs = {
            'channelId': self.ctx.channel.id,
            'messageType': content.message_type.value,
            'messageBody': str(content),
            'referencedMessageId': self.msg_id,
        }

        return await self._bot.client.send_public_message(**kwargs)

    async def edit(self, content: Union[str, MessageBody]):
        if isinstance(content, str):
            content = TextMessage(content)

        if self.msg_type != content.message_type:
            raise MessageTypeError([], self.msg_type.value)

        kwargs = {
            'messageId': self.msg_id,
            'messageBody': str(content)
        }

        return await self._bot.client.edit_public_message(**kwargs)

    async def delete(self, reason: str):
        ...

    async def fetch_emoji_list(self):
        ...

    async def fetch_emoji_user(self, emoji: str):
        ...

    async def add_reaction(self, emoji: str):
        ...

    async def delete_reaction(self, emoji: str, user_id: str):
        ...
