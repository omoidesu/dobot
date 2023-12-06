from dobot.eventMessage.message.component.channal import Channel
from dobot.eventMessage.message.component.island import Island
from dobot.eventMessage.message.component.user import User


class Context:
    _island: Island
    _channel: Channel
    _user: User

    def __init__(self, island: Island, channel: Channel, user: User):
        super().__init__()
        self._island = island
        self._channel = channel
        self._user = user

    @property
    def island(self):
        return self._island

    @property
    def channel(self):
        return self._channel

    @property
    def user(self):
        return self._user
