import asyncio
import os
from collections import ChainMap
from typing import Union

import aiofiles

from dobot.client import Client
from dobot.exception.argumentError import ArgumentError
from dobot.file.file.file import File
from dobot.file.file.image import Image
from dobot.functional import SingleClass, async_absolute_path


@SingleClass
class F:
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


    @async_absolute_path
    async def upload_image(self, file: Union[str, Image]):
        """
        单个图片的上传功能

        注意！ 如果传入为Image对象，极其建议初始化Image的时候加上 _path_label=图片的路径 的参数，保证图片是单例存在的

        :param file: 文件对象，可以是单纯的路径，也可以是Image对象
        """
        if isinstance(file, str):
            img: Image = self._file.add_image(file)
        else:
            img: Image = file
        # 对于相同路径下的Image对象，img是单例的，这里赋值增加可读性
        img: Image = await img.upload()
        return img

    @async_absolute_path
    async def __upload_image(self, file: Union[str, Image]):
        _key = file if isinstance(file, str) else file.path
        try:
            img: Image = await self.upload_image(file)
        except Exception as e:
            img: Exception = e
        return {
            _key: img
        }

    async def upload_image_list(self, file_list: Union[list, tuple]) -> dict:
        """
        批量上传图片，默认走单线程异步调用，所以会比for循环调用快很多
        :param file_list: 文件的list，list里面的类型可以是文件路径，也可以是Image对象，但是推荐从R中的get_image_by_path或者get_image拿到图片后再调用这个方法
        """
        # if any(abs_path.lower().endswith(ext) for ext in PICTURE_SUFFIX):
        # noinspection PyTypeChecker
        if any(isinstance(item, str) for item in file_list):
            # 如果全是字符串的情况，将路径变为绝对路径，生成新的file_list
            _file_list = []
            for path in file_list:
                _file_list.append(Image(path, _path_label=path))
            file_list = _file_list
        elif any(isinstance(item, Image) for item in file_list):
            pass
        else:
            raise ArgumentError("ArgumentError! file_list need str or Image type!")

        _buffer = []
        _gather_func = []
        for img in file_list:
            if img.path not in _buffer:
                _gather_func.append(self.__upload_image(img))
                _buffer.append(img.path)
        image_list = await asyncio.gather(*_gather_func)
        return dict(ChainMap(*image_list))
