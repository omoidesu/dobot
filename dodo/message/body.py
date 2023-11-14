import json

from dodo.const import MessageType


class MessageBody:
    content: str
    message_type: MessageType

    def __init__(self, content, message_type):
        self.content = content
        self.message_type = message_type

    def __str__(self):
        return json.dumps(self.dict())

    def dict(self):
        result = {}

        for k, v in self.__dict__.items():
            if k != 'message_type':
                result[k] = v

        return result


class TextMessage(MessageBody):
    def __init__(self, content):
        super().__init__(content, MessageType.TEXT)


class ImageMessage(MessageBody):
    url: str
    width: int
    height: int
    original: bool

    def __(self, url, width, height, original):
        super().__init__(url, MessageType.IMAGE)
        self.url = url
        self.width = width
        self.height = height
        self.original = original


class VideoMessage(MessageBody):
    url: str
    cover_url: str
    duration: int
    size: int

    def __init__(self, url, cover_url, duration, size):
        super().__init__(url, MessageType.VIDEO)
        self.url = url
        self.cover_url = cover_url
        self.duration = duration
        self.size = size


class ShareMessage(MessageBody):
    jump_url: str

    def __init__(self, jump_url):
        super().__init__(jump_url, MessageType.SHARE)
        self.jump_url = jump_url


class FileMessage(MessageBody):
    url: str
    name: str
    size: int

    def __init__(self, url, name, size):
        super().__init__(url, MessageType.FILE)
        self.url = url
        self.name = name
        self.size = size


class CardMessage(MessageBody):
    ...


class RedPacketMessage(MessageBody):
    type: int
    count: int
    total_amount: float
    receiver_type: int
    role_id: list


def parse_message_body(msg_type: str, event_body: dict) -> MessageBody:
    if msg_type == MessageType.TEXT.value:
        _message_body = event_body.get("messageBody", {})
        return TextMessage(_message_body.get("content", ""))
    else:
        ...
