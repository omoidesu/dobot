from pathlib import Path

from dobot.const import PICTURE_SUFFIX
from dobot.file.file.image import Image
from dobot.functional import SingleClass


@SingleClass
class File:
    """
    保存所有监控文件夹内的文件
    """
    _image: dict
    _file: dict
    _video: dict
    _audio: dict

    def __init__(self):
        self._image = {}
        self._file = {}
        self._video = {}
        self._audio = {}

    @staticmethod
    def __path_parser(path) -> str:
        return path.replace('\\', '/')

    async def __images_list(self, folder_path, base_path=None):
        """
        获取文件夹内所有图片，并输出绝对路径
        """
        folder = Path(folder_path)
        base_path = Path(base_path) if base_path else folder.resolve()

        for entry in folder.iterdir():
            if entry.is_file() and entry.suffix.lower() in PICTURE_SUFFIX:
                yield entry.resolve()
            elif entry.is_dir():
                async for image_path in self.__images_list(entry, base_path):
                    yield image_path

    async def _image_files(self, folder_path):
        """
        将所有文件保存到当前类中
        """
        async for image_path in self.__images_list(folder_path):
            _image_path = self.__path_parser(str(image_path))
            # TODO Dodo暂时仅支持图片
            self._image[_image_path] = Image(_image_path, _path_label=_image_path)

    def add_image(self, image_path) -> Image:
        """
        添加文件
        """
        if image_path not in self._image:
            self._image[self.__path_parser(image_path)] = Image(image_path, _path_label=image_path)
        return self._image[self.__path_parser(image_path)]

    def remove_image(self, image_path):
        """
        删除文件
        """
        self._image.pop(self.__path_parser(image_path))

    def reset_image(self, image_path):
        """
        添加文件
        """
        self._image[self.__path_parser(image_path)] = Image(image_path, _path_label=image_path)

    async def add_path(self, path):
        """
        当监控开始时获取所有的文件，保存到当前类中
        """
        # TODO Dodo目前仅支持图片
        await self._image_files(path)

    async def remove_path(self, path):
        """
        当监控结束时删除所有的文件
        """
        __remove_item = []
        for item in self._image:
            if item.startswith(self.__path_parser(path)):
                __remove_item.append(item)
        for __item in __remove_item:
            self._image.pop(__item)

    def get_image(self, img_with_path):
        """
        通过文件路径获取被R管理的文件对象
        """
        return self._image[img_with_path]

    def get_image_by_path(self, path):
        """
        通过文件夹路径获取被R管理的文件对象的list
        """
        __image_list = []
        for item in self._image:
            if item.startswith(self.__path_parser(path)):
                __image_list.append(self._image[item])
        return __image_list
