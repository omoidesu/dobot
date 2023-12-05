import aiofiles

from dobot.client import Client
from dobot.file.file.file import File
from dobot.functional import SingleClass


@SingleClass
class Uploader:
    """
    用于统一处理文件的方法，深度绑定DodoAPI
    """
    _file: File
    _client: Client

    def __init__(self):
        self._client = Client()

    @staticmethod
    async def open(path: str):
        async with aiofiles.open(path, mode='rb') as file:
            image_binary = await file.read()
            return image_binary

    async def upload_image(self, path):
        """
        上传图片
        """
        _image_binary = await self.open(path)
        _upload_params = {
            'file': (_image_binary)
        }
        # 上传图片
        res = await self._client.upload_image(**_upload_params)
        _data = res.get("data", {})
        print(_data)
        self._url = _data.get("url", "")
        self._height = _data.get("height", 0)
        self._width = _data.get("width", 0)
        self._if_upload = True