from dobot.exception.argumentError import ArgumentError


class BaseFile:
    def upload(self, file: bytes):
        """
        上传图片
        """
        raise ArgumentError("Invalid method! Only Image has upload method")