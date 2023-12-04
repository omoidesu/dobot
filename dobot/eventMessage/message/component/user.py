from dobot.exception.argumentError import InitializationError


class User:
    _id: str
    _nickname: str
    _personal_nickname: str
    _avatar: str
    _joined_at: str
    _sex: int
    _island_id: str

    def __init__(self, **kwargs):
        self._id = kwargs.get("id", "")
        if not self._id:
            raise InitializationError("dodo_id is required")
        self._nickname = kwargs.get("nickname", "")
        self._personal_nickname = kwargs.get("personal_nickname", "")
        self._avatar = kwargs.get("avatar", "")
        self._joined_at = kwargs.get("joined_at", "")
        self._sex = kwargs.get("sex", "")
        self._island_id = kwargs.get("island_id", "")

    @property
    def id(self):
        return self._id

    @property
    def nickname(self):
        return self._nickname

    @property
    def personal_nickname(self):
        return self._personal_nickname

    @property
    def avatar(self):
        return self._avatar

    @property
    def joined_at(self):
        return self._joined_at

    @property
    def sex(self):
        return self._sex

    @property
    def island_id(self):
        return self._island_id
