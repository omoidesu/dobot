from dodo.channel import Channel
from dodo.exception.argumentError import InitializationError
from dodo.user import User


class Island:
    _id: str
    _island_name: str
    _cover_url: str
    _member_count: int
    _online_count: int
    _description: str
    _default_channel: Channel
    _system_channel: Channel
    _owner_user: User
    _fetched: bool

    def __init__(self, **kwargs):
        self._id = kwargs.get("id", "")
        if not self._id:
            raise InitializationError("island_id is required")
        self._island_name = kwargs.get("island_name", "")
        self._cover_url = kwargs.get("cover_url", "")
        self._member_count = kwargs.get("member_count", "")
        self._online_count = kwargs.get("online_count", "")
        self._description = kwargs.get("description", "")
        self._default_channel = kwargs.get("default_channel", "")
        self._system_channel = kwargs.get("system_channel", "")
        self._owner_user = kwargs.get("owner_user", "")
        self._fetched = False

    @property
    def id(self):
        return self._id

    @property
    def island_name(self):
        return self._island_name

    @property
    def cover_url(self):
        return self._cover_url

    @property
    def member_count(self):
        return self._member_count

    @property
    def online_count(self):
        return self._online_count

    @property
    def description(self):
        return self._description

    @property
    def default_channel(self):
        return self._default_channel

    @property
    def system_channel(self):
        return self._system_channel

    @property
    def owner_user(self):
        return self._owner_user

    @property
    def fetched(self):
        return self._fetched

    async def fetch_island(self):
        ...
