import re

from dodo.const import MENTION_PATTERN


class Content(str):
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

    def __str__(self):
        return self.content
