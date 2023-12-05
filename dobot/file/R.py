import os.path
import sys

from dobot.const import WINDOWS, LINUX
from dobot.exception.argumentError import SystemKernelError
from dobot.file.file.file import File
from dobot.file.file.image import Image
from dobot.file.monitor.baseFileMonitor import BaseFileMonitor
from dobot.file.monitor.windowsFileMonitor import WindowsFileMonitor
from dobot.functional import SingleClass


@SingleClass
class R:
    """
    用于管理内部文件
    """

    @staticmethod
    def _get_platform():
        if sys.platform.startswith('win'):
            return WINDOWS
        elif sys.platform.startswith('linux'):
            return LINUX
        else:
            raise SystemKernelError("SystemKernelError! dobot only support Windows and Linux now")

    @staticmethod
    def __absolute_path(func):
        def wrapper(self, path: str):
            _abs_path = os.path.abspath(path)
            return func(self, _abs_path)

        return wrapper

    _monitor: BaseFileMonitor = WindowsFileMonitor() if _get_platform() == WINDOWS else None
    _file: File

    def __init__(self):
        self._file = File()

    @__absolute_path
    async def add_path(self, path):
        """
        添加监控的路径，从一添加进来的瞬间这里就开始监控了
        """
        await self._monitor.add_path(path)
        return self

    @__absolute_path
    async def remove_path(self, path):
        """
        移除监控的路径
        """
        await self._monitor.remove_path(path)
        return self

    @__absolute_path
    def get_image(self, img_with_path) -> Image:
        """
        根据文件绝对路径，获取文件对象
        """
        return self._file.get_image(img_with_path)

    @__absolute_path
    def get_image_by_path(self, path) -> list:
        """
        根据文件夹路径，获取文件夹内所有文件对象
        """
        return self._file.get_image_by_path(path)
