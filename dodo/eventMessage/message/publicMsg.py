from typing import Union

import emoji as emoji_lib

from dodo.client import Client
from dodo.const import MessageType
from dodo.eventMessage.message.baseMsg import BaseMsg
from dodo.eventMessage.message.component.content import Content
from dodo.eventMessage.message.component.member import Member
from dodo.eventMessage.message.component.personal import Personal
from dodo.eventMessage.message.context import Context
from dodo.exception.argumentError import ArgumentError
from dodo.functional import CachedProperty


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
        if message_body is None:
            message_body = {}
        self._content = Content(message_body.get('content', ''))
        if content:
            self._content = Content(content)
        self._client = Client()

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
        if len(emoji) != 1:
            target_emoji = emoji_lib.emojize(emoji, language='alias')
            if target_emoji == emoji:
                raise ArgumentError("emoji must be a single emoji or a shortcode")
        else:
            target_emoji = emoji

        kwargs = {
            'messageId': self._message_id,
            'emoji': {'type': 1, 'id': str(ord(target_emoji))}
        }

        return await self._client.add_public_message_reaction(**kwargs)
