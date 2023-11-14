from dodo.exception.argumentError import InitializationError


class User:
    _id: str
    _nickname: str
    _personal_nickname: str
    _avatar: str
    _joined_at: str
    _sex: int
    _level: int
    _is_bot: int
    _online_device: int
    _online_status: int
    _island_id: str
    _fetched: bool

    def __init__(self, **kwargs):
        self._id = kwargs.get("id", "")
        if not self._id:
            raise InitializationError("dodo_id is required")
        self._nickname = kwargs.get("nickname", "")
        self._personal_nickname = kwargs.get("personal_nickname", "")
        self._avatar = kwargs.get("avatar", "")
        self._joined_at = kwargs.get("joined_at", "")
        self._sex = kwargs.get("sex", "")
        self._level = kwargs.get("level", "")
        self._is_bot = kwargs.get("is_bot", "")
        self._online_device = kwargs.get("online_device", "")
        self._online_status = kwargs.get("online_status", "")
        self._island_id = kwargs.get("island_id", "")
        self._fetched = False

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
    def level(self):
        return self._level

    @property
    def is_bot(self):
        return self._is_bot

    @property
    def online_device(self):
        return self._online_device

    @property
    def online_status(self):
        return self._online_status

    @property
    def island_id(self):
        return self._island_id

    @property
    def fetched(self):
        return self._fetched

    async def fetch_user(self):
        ...
