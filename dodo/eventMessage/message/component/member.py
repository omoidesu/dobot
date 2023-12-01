class Member:
    def __init__(self, member: dict):
        self._nick_name = member.get('nickName', '')
        self._join_time = member.get('joinTime', '')

    @property
    def nick_name(self):
        return self._nick_name

    @property
    def join_time(self):
        return self._join_time