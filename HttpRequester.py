import asyncio

from aiohttp import ClientSession

from AuthCell import AuthCell
from DodoApiEnum import DodoApiEnum
from Logging import MyLogger
from interface.LogAbstractObject import LogAbstractObject
from wrapper.ClassLoggerWrapper import ClassLoggerWrapper

__all__ = ["HttpRequester", "POST", "GET", "PUT", "DELETE"]

POST = "POST"
GET = "GET"
PUT = "PUT"
DELETE = "DELETE"

logger = MyLogger()

@ClassLoggerWrapper
class HttpRequester(LogAbstractObject):
    _print_time_logger: bool = False
    _cs: ClientSession = None

    def __init__(self, print_time_logger: bool = None):
        self._auth_cell = AuthCell()
        if print_time_logger is not None:
            self._print_time_logger = print_time_logger

    def time_logger_wrapper(self, print_time_logger: bool = False):
        def decorator(func):
            def wrapper(*args, **kwargs):
                pass

            return wrapper

        return decorator

    def async_time_logger_wrapper(self, print_time_logger: bool = False):
        def decorator(func):
            def wrapper(*args, **kwargs):
                pass

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
            async with self._cs.request(method, f'{DodoApiEnum.BASE_API_URL.value}{route}', **params) as res:
                if res.content_type == 'application/json':
                    rsp = await res.json()
                    # if rsp['code'] != 0:
                    #     raise HttpRequester.APIRequestFailed(method, route, params, rsp['code'], rsp['message'])
                    # rsp = rsp['data']
                else:
                    rsp = await res.read()

                logger.debug(f'{method} {route}: rsp: {rsp}')
                return rsp

        return await request(method, route, **params)

    class APIRequestFailed(Exception):
        """
        This class is copied from khl.py /khl/requester.py
        """

        def __init__(self, method, route, params, err_code, err_message):
            super().__init__()
            self.method = method
            self.route = route
            self.params = params
            self.err_code = err_code
            self.err_message = err_message

        def __str__(self):
            return f"Requesting '{self.method} {self.route}' failed with {self.err_code}: {self.err_message}"



if __name__ == "__main__":
    a = AuthCell("83199120", "ODMxOTkxMjA.77-9LAnvv70.4-jInox-uI8LTujPQZASLRGcxd_mn5twL-55m0LK7xc")
    h = HttpRequester(True)
    print(a.bot_id)
    asyncio.run(h.request("POST", DodoApiEnum.WS_CLIENT_GETTER_URL.value, headers={"Content-Type": "application/json"}))
