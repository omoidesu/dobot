from abc import ABC
from typing import Union

from dodo.client import Client
from dodo.const import MessageType
from dodo.interface.bodyAbstractObject import Body
from dodo.message.context import Context


class Message(ABC):
    _client: Client
    msg_id: str
    msg_type: MessageType
    ctx: Context
    body: Body
    mention: tuple

    async def reply(self, content: Union[str, Body]):
        ...

    async def edit(self, content: Union[str, Body]):
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
