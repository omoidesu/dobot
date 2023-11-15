from abc import ABC
from typing import Union

from dodo.const import MessageType
from dodo.message.body import MessageBody
from dodo.message.context import Context


class Message(ABC):
    msg_id: str
    msg_type: MessageType
    ctx: Context
    body: MessageBody
    mention: tuple

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
