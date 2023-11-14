import re
from typing import Union

import emoji as emoji_lib

from dodo.cert import AuthInfo
from dodo.channel import Channel
from dodo.client import Client
from dodo.const import MENTION_PATTERN, MessageType
from dodo.exception.argumentError import ArgError
from dodo.exception.typeError import MessageTypeError
from dodo.interface.message import Message
from dodo.island import Island
from dodo.message.body import MessageBody, TextMessage, parse_message_body
from dodo.message.context import Context
from dodo.user import User


class PublicMessage(Message):
    mention: tuple

    def __init__(self, event_body: dict):
        self._client = Client()
        self.msg_id = event_body.get("messageId", '')
        self.msg_type = event_body.get('messageType', '')
        self.ctx = PublicMessage._context_builder(event_body)
        _body = parse_message_body(event_body["messageType"], event_body)
        self.body = _body

        if self.body.message_type == MessageType.TEXT:
            self.mention = tuple(set(re.findall(MENTION_PATTERN, self.body.content)))

    @staticmethod
    def _context_builder(event_body: dict) -> Context:
        personal_info: dict = event_body.get("personal", {})
        member_info: dict = event_body.get("member", {})
        author = User(
            id=event_body.get("dodoSourceId"),
            personal_nickname=personal_info.get("nickName", ""),
            avatar=personal_info.get("avatarUrl", ""),
            sex=personal_info.get("sex", -1),
            island_id=event_body.get("islandSourceId", ""),
            nickname=member_info.get("nickName", ""),
            joined_at=member_info.get("joinTime", "")
        )
        channel = Channel(id=event_body.get("channelId", ""))
        island = Island(id=event_body.get("islandSourceId", ""))

        return Context(island, channel, author)

    async def reply(self, content: Union[str, MessageBody]) -> Message:
        if isinstance(content, str):
            content = TextMessage(content)

        kwargs = {
            'channelId': self.ctx.channel.id,
            'messageType': content.message_type.value,
            'messageBody': content.dict(),
            'referencedMessageId': self.msg_id,
        }

        response = await self._client.send_public_message(**kwargs)
        event_body = response.get('data', {})
        event_body['messageType'] = content.message_type.value
        event_body['channelId'] = self.ctx.channel.id
        event_body['islandSourceId'] = self.ctx.island.id
        event_body['dodoSourceId'] = AuthInfo.get_instance().me

        return PublicMessage(event_body)

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
        if len(emoji) != 1:
            target_emoji = emoji_lib.emojize(emoji, language='alias')
            if target_emoji == emoji:
                raise ArgError("emoji must be a single emoji or a shortcode")
        else:
            target_emoji = emoji

        kwargs = {
            'messageId': self.msg_id,
            'emoji': {'type': 1, 'id': str(ord(target_emoji))}
        }

        return await self._client.add_public_message_reaction(**kwargs)

    async def delete_reaction(self, emoji: str, user_id: str):
        ...
