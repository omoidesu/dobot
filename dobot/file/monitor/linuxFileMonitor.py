from dobot.file.monitor.baseFileMonitor import BaseFileMonitor
from dobot.functional import SingleClass


@SingleClass
class LinuxFileMonitor(BaseFileMonitor):
    """
    linux特化的类，用于区分可能存在的部分差异
    """
    def __init__(self, path_name):
        super().__init__(path_name)
