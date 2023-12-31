from typing import Union

from dobot.client import Client
from dobot.const import MessageType
from dobot.eventMessage.message.baseMsg import BaseMsg
from dobot.eventMessage.message.component.content import Content
from dobot.eventMessage.message.component.member import Member
from dobot.eventMessage.message.component.personal import Personal
from dobot.eventMessage.message.context import Context
from dobot.functional import CachedProperty


class PublicMsg(BaseMsg):
    _MESSAGE_TYPE = MessageType.TEXT.value
    _island_source_id: str
    _channel_id: str
    _dodo_source_id: str
    _message_id: str
    _personal: Personal
    _member: Member
    _ctx: Context
    _client: Client

    def __init__(self, message_body=None, content: str = ''):
        super().__init__()
        if message_body is None:
            message_body = {}
        self._content = Content(message_body.get('content', ''))
        if content:
            self._content = Content(content)

    def dict(self):
        return {
            "content": self.content
        }

    @property
    def content(self):
        return self._content

    @CachedProperty
    def mention(self):
        """
        获取消息的@信息
        """
        return self._content.mention,

    @CachedProperty
    def pre_mention(self):
        """
        获取消息prefix之前的@信息
        """
        return self._content.pre_mention

    async def send(self, content: Union[str, BaseMsg]) -> dict:
        if isinstance(content, str):
            content = PublicMsg(content=content)

        kwargs = {
            'channelId': self.ctx.channel.id,
            'messageType': content._MESSAGE_TYPE,
            'messageBody': content.dict()
        }

        return await self._client.send_public_message(**kwargs)

    async def reply(self, content: Union[str, BaseMsg]) -> dict:
        if isinstance(content, str):
            content = PublicMsg(content=content)

        kwargs = {
            'channelId': self.ctx.channel.id,
            'messageType': content._MESSAGE_TYPE,
            'messageBody': content.dict(),
            'referencedMessageId': self.message_id,
        }

        return await self._client.send_public_message(**kwargs)

    async def edit(self, content: Union[str, BaseMsg]) -> dict:
        if isinstance(content, str):
            content = PublicMsg(content=content)

        kwargs = {
            'messageId': self.message_id,
            'messageBody': content.dict()
        }

        return await self._client.edit_public_message(**kwargs)

    async def delete(self, reason: str, message_id: str = None) -> dict:
        kwargs = {
            'messageId': self.message_id if message_id is None else message_id,
            'reason': reason
        }

        return await self._client.delete_public_message(**kwargs)

    async def top(self):
        kwargs = {
            'messageId': self._message_id,
        }

        return await self._client.top_public_message(**kwargs)

    async def cancel_top(self):
        kwargs = {
            'messageId': self._message_id,
        }

        return await self._client.cancel_top_public_message(**kwargs)

    async def add_reaction(self, emoji: str):
        target_emoji = self._parse_emoji(emoji)

        kwargs = {
            'messageId': self._message_id,
            'emoji': {'type': 1, 'id': str(ord(target_emoji))}
        }

        return await self._client.add_public_message_reaction(**kwargs)

    async def remove_reaction(self, emoji: str):
        target_emoji = self._parse_emoji(emoji)

        kwargs = {
            'messageId': self._message_id,
            'emoji': {'type': 1, 'id': str(ord(target_emoji))}
        }

        return await self._client.remove_public_message_reaction(**kwargs)
