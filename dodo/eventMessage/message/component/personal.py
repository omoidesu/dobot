class Personal:
    def __init__(self, personal: dict):
        self._nick_name = personal.get('nickName', '')
        self._avatar_url = personal.get('avatarUrl', '')
        self._sex = personal.get('sex', -1)

    @property
    def nick_name(self):
        return self._nick_name

    @property
    def avatar_url(self):
        return self._avatar_url

    @property
    def sex(self):
        return self._sex