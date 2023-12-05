import asyncio
import json

from aiohttp import ClientSession
from urllib3 import encode_multipart_formdata

from .cert import AuthInfo
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
        self._auth_cell = AuthInfo.get_instance()
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

    async def request(self, route: str, **kwargs):
        @self.async_time_logger_wrapper(self._print_time_logger)
        async def do_request(route: str, **kwargs):
            _headers = AuthInfo.get_instance().header
            _type = kwargs.pop("_type", None)
            if _type is not None and _type == "form-data":
                """
                参照@AlanStar233 的文件上传请求头和数据的处理方式
                """
                form_data = {'file': kwargs.get("file")}
                encode_data = encode_multipart_formdata(form_data)
                _data = encode_data[0]
                _headers["Content-Type"] = encode_data[1]
            else:
                _data = json.dumps(kwargs)

            if self._cs is None:
                self._cs = ClientSession()

            async with self._cs.post(route, data=_data, headers=_headers) as response:
                if response.status != 200:
                    raise RequestError(response.status, route)

                data = await response.json()
                status = data.get("status", -9999)
                if status != 0:
                    raise ApiRequestError(response.status, route, kwargs, status, data.get("message", ""))

            return data

        return await do_request(route, **kwargs)
