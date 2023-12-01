from dodo.exception.argumentError import InitializationError


class Channel:
    _id: str

    def __init__(self, **kwargs):
        self._id = kwargs.get("id", "")
        if not self._id:
            raise InitializationError("InitializationError! channel_id is required")

    @property
    def id(self):
        return self._id
