from typing import Union

from .const import Route
from .exception.typeError import MessageTypeError
from .request import HttpRequester


class Client:
    _gateway: HttpRequester
    __allow_message_type__ = [1, 2, 3, 6]

    def __init__(self, log_time: bool = False):
        self._gateway = HttpRequester(log_time)

    async def request(self, route: Union[Route, str], **kwargs):
        if isinstance(route, Route):
            route = route.value

        return await self._gateway.request(route, **kwargs)

    async def send_public_message(self, **kwargs):
        if kwargs.get('messageType', -1) not in self.__allow_message_type__:
            raise MessageTypeError(self.__allow_message_type__)

        return await self.request(Route.SET_CHANNEL_MESSAGE_SEND, **kwargs)

    async def edit_public_message(self, **kwargs):
        return await self.request(Route.SET_CHANNEL_MESSAGE_EDIT, **kwargs)

    async def delete_public_message(self, **kwargs):
        return await self.request(Route.SET_CHANNEL_MESSAGE_WITHDRAW, **kwargs)

    async def top_public_message(self, **kwargs):
        kwargs["operateType"] = 1
        return await self.request(Route.SET_CHANNEL_MESSAGE_TOP, **kwargs)

    async def cancel_top_public_message(self, **kwargs):
        kwargs["operateType"] = 0
        return await self.request(Route.SET_CHANNEL_MESSAGE_TOP, **kwargs)

    async def add_public_message_reaction(self, **kwargs):
        return await self.request(Route.SET_CHANNEL_MESSAGE_REACTION_ADD, **kwargs)

    async def remove_public_message_reaction(self, **kwargs):
        return await self.request(Route.SET_CHANNEL_MESSAGE_REACTION_REMOVE, **kwargs)

    async def upload_image(self, **kwargs):
        kwargs["_type"] = "form-data"
        return await self.request(Route.SET_RESOURCE_PICTURE_UPLOAD, **kwargs)
