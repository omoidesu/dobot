import os.path

import aiofiles

from dobot.client import Client
from dobot.file.file.baseFile import BaseFile
from dobot.functional import CachedClass, CachedProperty


@CachedClass
class Image(BaseFile):
    _client: Client
    _path: str
    _url: str
    _height: int
    _width: int
    _if_upload: bool

    def __init__(self, path: str):
        self._client = Client()
        self._path = os.path.abspath(path).replace("\\", '/')
        self._file_name = os.path.basename(path)
        self._if_upload = False

    def __hash__(self):
        return self._path.__hash__()

    @property
    def path(self):
        return self._path

    async def open(self):
        async with aiofiles.open(self._path, mode='rb') as file:
            image_binary = await file.read()
            return image_binary

    async def upload(self):
        if self._if_upload:
            # 如果上传过了返回对象本身
            return self

        # 如果没上传过上传后返回对象本身
        _image_binary = await self.open()
        _upload_params = {
            'file': (self._file_name, _image_binary)
        }
        # 上传图片
        res = await self._client.upload_image(**_upload_params)
        _data = res.get("data", {})
        print(_data)
        self._url = _data.get("url", "")
        self._height = _data.get("height", 0)
        self._width = _data.get("width", 0)
        self._if_upload = True
        return self
