from dodo.exception.argumentError import InitializationError


class Channel:
    _id: str
    _channel_name: str
    _channel_type: int
    _island_id: str
    _is_default: bool
    _group_id: str
    _group_name: str
    _fetched: bool

    def __init__(self, **kwargs):
        self._id = kwargs.get("id", "")
        if not self._id:
            raise InitializationError("channel_id is required")
        self._channel_name = kwargs.get("channel_name", "")
        self._channel_type = kwargs.get("channel_type", "")
        self._island_id = kwargs.get("island_id", "")
        self._is_default = kwargs.get("is_default", "")
        self._group_id = kwargs.get("group_id", "")
        self._group_name = kwargs.get("group_name", "")
        self._fetched = False

    @property
    def id(self):
        return self._id

    @property
    def channel_name(self):
        return self._channel_name

    @property
    def channel_type(self):
        return self._channel_type

    @property
    def island_id(self):
        return self._island_id

    @property
    def is_default(self):
        return self._is_default

    @property
    def group_id(self):
        return self._group_id

    @property
    def group_name(self):
        return self._group_name

    @property
    def fetched(self):
        return self._fetched

    async def fetch_channel(self):
        ...
