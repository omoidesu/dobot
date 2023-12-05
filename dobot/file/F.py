from typing import BinaryIO, Union

from dobot.functional import SingleClass


@SingleClass
class F:
    """
    文件工厂，用于存放所有监控的文件，并且提供对应的处理方法
    """

    _file_name: str
    _path: str
    _upload_image_list: list
    _complete_image_list: list
    _f: Union[None, BinaryIO]
    _f_map: dict

    def __init__(self, file_name: str, path: str = ''):
        self._f = None
        self._file_name = file_name
        self._path = path

    def __del__(self):
        print("del")
        if self._f is not None:
            self._f.close()

    def __enter__(self):
        self._f = self.open(self._path + self._file_name, "rb")
        return self._f

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("close")
        self._f.close()

    def open(self, file_name: str, path: str = ''):
        """
        打开文件
        """
        # 判断map中是否有该文件，如果有就pass掉
        print("我不应该被调用")
        if file_name not in self._f_map:
            self._f_map[file_name] = open(path + file_name, "rb")
        self._f = open(path + file_name, "rb")
        return self._f


if __name__ == "__main__":
    f = F("image.py")
