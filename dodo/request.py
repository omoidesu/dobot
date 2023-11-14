import asyncio
import json

from aiohttp import ClientSession

from .cert import AuthCell
from .const import Route
from .exception import ApiRequestError, RequestError
from .interface.LogAbstractObject import LogAbstractObject
from .log import MyLogger
from .wrapper.ClassLoggerWrapper import class_logger_wrapper

logger = MyLogger()


@class_logger_wrapper
class HttpRequester(LogAbstractObject):
    _print_time_logger: bool = False
    _cs: ClientSession = None

    def __init__(self, print_time_logger: bool = False):
        self._auth_cell = AuthCell.get_instance()
        if print_time_logger:
            self._print_time_logger = print_time_logger

    def __del__(self):
        if self._cs is not None:
            asyncio.gather(self._cs.close())

    def time_logger_wrapper(self, print_time_logger: bool = False):
        def decorator(func):
            def wrapper(*args, **kwargs):
                ...

            return wrapper

        return decorator

    def async_time_logger_wrapper(self, print_time_logger: bool = False):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                ...

            return wrapper

        return decorator

    """async def request(self, method: str, route: str, **params):
        @self.async_time_logger_wrapper(self._print_time_logger)
        async def request(method: str, route: str, **params):
            headers = params.pop('headers', {})
            params['headers'] = headers

            headers['Authorization'] = f'Bot {self._auth_cell.bot_id}.{self._auth_cell.bot_token}'
            if self._cs is None:
                self._cs = ClientSession()
            print(params)
            async with self._cs.request(method, f'{Route.BASE_API_URL}{route}', **params) as resp:
                if resp.content_type == 'application/json':
                    rsp = await resp.json()
                    # if rsp['code'] != 0:
                    #     raise HttpRequester.APIRequestFailed(method, route, params, rsp['code'], rsp['message'])
                    # rsp = rsp['data']
                else:
                    rsp = await resp.read()

                logger.debug(f'{method} {route}: rsp: {rsp}')
                return rsp

        return await request(method, route, **params)"""

    async def request(self, route: str, **kwargs):
        @self.async_time_logger_wrapper(self._print_time_logger)
        async def do_request(route: str, **kwargs):
            print("do_request")
            if self._cs is None:
                self._cs = ClientSession()

            data = json.dumps(kwargs)

            async with self._cs.post(route, data=data, headers=AuthCell.get_instance().header) as response:
                if response.status != 200:
                    raise RequestError(response.status, route)

                data = await response.json()
                status = data.get("status", -9999)
                if status != 0:
                    raise ApiRequestError(response.status, route, kwargs, status, data.get("message", ""))

            return data

        return await do_request(route, **kwargs)


if __name__ == "__main__":
    async def run():
        AuthCell("83199120", "ODMxOTkxMjA.77-9LAnvv70.4-jInox-uI8LTujPQZASLRGcxd_mn5twL-55m0LK7xc")
        h = HttpRequester(True)
        # await h.request("POST", Route.WS_CLIENT_GETTER_URL, headers={"Content-Type": "application/json"})
        bot_info = await h.request(Route.GET_BOT_INFO.value)
        print(bot_info)


    asyncio.new_event_loop().run_until_complete(run())
