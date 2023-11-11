import asyncio

from aiohttp import ClientSession

from AuthCell import AuthCell
from DodoApiEnum import DodoApiEnum
from Logging import MyLogger
from interface.LogAbstractObject import LogAbstractObject
from wrapper.ClassLoggerWrapper import class_logger_wrapper

__all__ = ["HttpRequester", "POST", "GET", "PUT", "DELETE"]

POST = "POST"
GET = "GET"
PUT = "PUT"
DELETE = "DELETE"

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

    async def request(self, method: str, route: str, **params):
        @self.async_time_logger_wrapper(self._print_time_logger)
        async def request(method: str, route: str, **params):
            headers = params.pop('headers', {})
            params['headers'] = headers

            headers['Authorization'] = f'Bot {self._auth_cell.bot_id}.{self._auth_cell.bot_token}'
            if self._cs is None:
                self._cs = ClientSession()
            print(params)
            async with self._cs.request(method, f'{DodoApiEnum.BASE_API_URL.value}{route}', **params) as resp:
                if resp.content_type == 'application/json':
                    rsp = await resp.json()
                    # if rsp['code'] != 0:
                    #     raise HttpRequester.APIRequestFailed(method, route, params, rsp['code'], rsp['message'])
                    # rsp = rsp['data']
                else:
                    rsp = await resp.read()

                logger.debug(f'{method} {route}: rsp: {rsp}')
                return rsp

        return await request(method, route, **params)


if __name__ == "__main__":
    async def run():
        a = AuthCell("83199120", "ODMxOTkxMjA.77-9LAnvv70.4-jInox-uI8LTujPQZASLRGcxd_mn5twL-55m0LK7xc")
        h = HttpRequester(True)
        await h.request("POST", DodoApiEnum.WS_CLIENT_GETTER_URL.value, headers={"Content-Type": "application/json"})


    asyncio.new_event_loop().run_until_complete(run())
