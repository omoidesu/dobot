from dobot.file.file.baseFile import BaseFile
from dobot.functional import CachedClass


@CachedClass
class Image(BaseFile):
    _path: str
    _url: str
    _height: int
    _width: int
    _if_upload: bool
    def __init__(self,path: str):
        self._path = path

