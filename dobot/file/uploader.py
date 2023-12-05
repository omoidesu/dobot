from dobot.file.file.file import File
from dobot.functional import SingleClass


@SingleClass
class Uploader:
    """
    用于统一处理文件的方法，深度绑定DodoAPI
    """
    _file: File
