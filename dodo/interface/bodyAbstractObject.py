from abc import ABC

from dodo.const import MessageType


class Body(ABC):
    content: str
    message_type: MessageType


    def __str__(self):
        ...

    def dict(self):
        ...