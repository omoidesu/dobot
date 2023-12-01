from typing import Union

from dodo.client import Client
from dodo.const import MessageType
from dodo.eventMessage.message.baseMsg import BaseMsg
from dodo.eventMessage.message.component.content import Content
from dodo.eventMessage.message.context import Context
from dodo.functional import CachedProperty


class PublicMsg(BaseMsg):
    _MESSAGE_TYPE = MessageType.TEXT.value
    _ctx: Context
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