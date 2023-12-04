from typing import Union

from dodo.client import Client
from dodo.eventMessage.message.component.member import Member
from dodo.eventMessage.message.component.personal import Personal
from dodo.eventMessage.message.context import Context
from dodo.exception.argumentError import ArgumentError
from dodo.functional import CachedProperty


class BaseMsg:
    _MESSAGE_TYPE: int
    _island_source_id: str
    _channel_id: str
    _dodo_source_id: str
    _message_id: str
    _personal: Personal
    _member: Member
    _ctx: Context
    _client: Client

    @property
    def ctx(self):
        return self._ctx

    @ctx.setter
    def ctx(self, ctx: Context):
        self._ctx = ctx

    @property
    def message_id(self):
        return self._message_id

    @message_id.setter
    def message_id(self, message_id: str):
        self._message_id = message_id

    @CachedProperty
    def mention(self):
        """
        获取消息的@信息
        """
        raise ArgumentError("Invalid Argument! Only PublicMsg has mention argument")

    @CachedProperty
    def pre_mention(self):
        """
        获取消息prefix之前的@信息
        """
        raise ArgumentError("Invalid Argument! Only PublicMsg has mention argument")

    async def reply(self, content):
        """
        回复消息
        """
        raise ArgumentError("Invalid method! Only msg event has reply method")

    async def edit(self, content):
        """
        编辑消息
        """
        raise ArgumentError("Invalid method! Only msg event has edit method")

    async def delete(self, reason, message_id: str = None):
        """
        撤回消息
        """
        raise ArgumentError("Invalid method! Only msg event has delete method")

    async def add_reaction(self, emoji: str):
        """
        添加表情反应
        """
        raise ArgumentError("Invalid method! Only msg event has add_reaction method")
