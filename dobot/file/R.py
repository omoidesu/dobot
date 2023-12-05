import sys

from dobot.const import WINDOWS, LINUX
from dobot.exception.argumentError import SystemKernelError
from dobot.file.monitor.baseFileMonitor import BaseFileMonitor
from dobot.file.monitor.windowsFileMonitor import WindowsFileMonitor
from dobot.functional import SingleClass


def _get_platform():
    if sys.platform.startswith('win'):
        return WINDOWS
    elif sys.platform.startswith('linux'):
        return LINUX
    else:
        raise SystemKernelError("SystemKernelError! dobot only support Windows and Linux now")

@SingleClass
class R:
    """
    用于管理内部文件
    """
    _monitor: BaseFileMonitor = WindowsFileMonitor() if _get_platform() == WINDOWS else None

    @staticmethod
    def _get_platform():
        if sys.platform.startswith('win'):
            return WINDOWS
        elif sys.platform.startswith('linux'):
            return LINUX
        else:
            raise SystemKernelError("SystemKernelError! dobot only support Windows and Linux now")

    def __init__(self):
        pass

    async def add_path(self, path):
        """
        添加监控的路径，从一添加进来的瞬间这里就开始监控了
        """
        return await self._monitor.add_path(path)

    async def remove_path(self, path):
        """
        移除监控的路径
        """
        return await self._monitor.remove_path(path)