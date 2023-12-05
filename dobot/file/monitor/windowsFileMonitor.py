from dobot.file.monitor.baseFileMonitor import BaseFileMonitor
from dobot.functional import SingleClass


@SingleClass
class WindowsFileMonitor(BaseFileMonitor):
    """
    windows特化的类，用于区分可能存在的部分差异
    """

    def __init__(self):
        super().__init__()

    def __set_name__(self, owner, name):
        if self._name is None:
            self._name = name
        elif name != self._name:
            raise TypeError(
                "Cannot assign the same property to two different names "
                "(%r and %r)." % (self._name, name)
            )


if __name__ == "__main__":
    class MyClass:
        def __init__(self):
            self.a = WindowsFileMonitor()


    my_instance = MyClass()
