import asyncio
from typing import Union

import watchgod

from dobot.const import PICTURE_SUFFIX, FILE_CREATED, FILE_DELETED
from dobot.file.file.file import File
from dobot.interface.AsyncRegisterObject import AsyncRegisterObject
from dobot.log import MyLogger

logger = MyLogger()


class BaseFileMonitor(AsyncRegisterObject):
    """
    监控windows内部文件的类
    """

    _task: dict
    _file_buffer: dict
    _name: Union[str, None]
    _file: File

    def __init__(self):
        self._name = None
        self._task = {}
        self._file = File()

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name
        elif name != self._name:
            raise TypeError(
                "Cannot assign the same property to two different names "
                "(%r and %r)." % (self._name, name)
            )

    @staticmethod
    def _map_action(action):
        """
        windows操作系统的操作映射
        """
        action_mapping = {
            1: 'created',
            2: 'modified',
            3: 'deleted',
            4: 'renamed',
            32768: 'unknown'  # 0x8000
        }
        return action_mapping.get(action, 'unknown')

    def on_file_change(self, file_name, action):
        """
        文件操作的回调函数
        """
        # TODO 现在只保存了图片类型的文件，后续需要添加其他类型的文件
        logger.debug(f"File {file_name} has been {self._map_action(action)}")
        if any(file_name.lower().endswith(ext) for ext in PICTURE_SUFFIX):
            if action == FILE_CREATED:
                self._file.add_image(file_name)
            elif action == FILE_DELETED:
                self._file.remove_image(file_name)
            else:
                self._file.reset_image(file_name)

    async def async_directory_monitoring(self, directory_path):
        """
        异步监控文件的方法
        :return:
        """
        async for changes in watchgod.awatch(directory_path):
            # noinspection PyTypeChecker
            for action, file_name in changes:
                self.on_file_change(file_name, action)

    async def add_path(self, path: Union[str, list, tuple]):
        """
        添加监控的路径，从一添加进来的瞬间这里就开始监控了
        """
        if isinstance(path, str) and path not in self._task:
            task = asyncio.create_task(self.async_directory_monitoring(path))
            self._task[path] = task
            await self._file.add_path(path)
        elif isinstance(path, (list, tuple)):
            for _path in path:
                if _path not in self._task:
                    task = asyncio.create_task(self.async_directory_monitoring(_path))
                    self._task[_path] = task
                    await self._file.add_path(_path)

    async def remove_path(self, path: Union[str, list, tuple]):
        """
        移除监控的路径，同时停止监控
        """
        if isinstance(path, str) and path in self._task:
            task = self._task.pop(path)
            task.cancel()
            await self._file.remove_path(path)
        elif isinstance(path, (list, tuple)):
            for _path in path:
                if _path in self._task:
                    task = self._task.pop(_path)
                    task.cancel()
                    await self._file.remove_path(_path)

    def run(self, *args, **kwargs):
        pass
