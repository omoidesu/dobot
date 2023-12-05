from dobot.client import Client
from dobot.exception.argumentError import ArgumentError


class BaseFile:
    _client: Client

    def upload(self):
        """
        上传图片
        """
        raise ArgumentError("Invalid method! Only Image has upload method")
