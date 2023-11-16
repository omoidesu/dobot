import json
import re

from dodo.const import MessageType, MENTION_PATTERN


class Content:
    pre_mention: tuple
    prefix: str
    content: str
    content_list: list
    mention: tuple

    def __init__(self, content_msg):
        self.content = content_msg.strip()
        self.content_list = []
        _msg_ls = self.content.split(' ')
        _pre_flag = True
        _pre_mention_ls = []
        for item in _msg_ls:
            if _pre_flag and item.startswith('<@!'):
                _pre_mention_ls.append(item[3:-1])
            else:
                _pre_flag = False
                if not hasattr(self, 'prefix'):
                    self.prefix = item
                else:
                    self.content_list.append(item)
        self.pre_mention = tuple(_pre_mention_ls)
        self.mention = tuple(set(re.findall(MENTION_PATTERN, self.content)))

    def __repr__(self):
        return self.content

class MessageBody:
    content_info: Content
    content: str
    message_type: MessageType

    def __init__(self, content, message_type):
        self.content_info = Content(content)
        self.content = content
        self.message_type = message_type

    def __str__(self):
        return json.dumps(self.dict())

    def dict(self):
        result = {}

        for k, v in self.__dict__.items():
            if k not in ('message_type', 'content_info'):
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
