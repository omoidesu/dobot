class Context:
    _island: Island
    _channel: Channel
    _author: User

    def __init__(self, island: Island, channel: Channel, author: User):
        self._island = island
        self._channel = channel
        self._author = author

    @property
    def island(self):
        return self._island

    @property
    def channel(self):
        return self._channel

    @property
    def author(self):
        return self._author
