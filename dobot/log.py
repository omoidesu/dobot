import logging

__all__ = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'MyLogger']

NOTSET: int = logging.NOTSET
DEBUG: int = logging.DEBUG
INFO: int = logging.INFO
WARNING: int = logging.WARNING
ERROR: int = logging.ERROR
CRITICAL: int = logging.CRITICAL


class MyLogger(logging.Logger):

    def __init__(self):
        # 设置日志的名字、日志的收集级别
        super().__init__("test_api", logging.DEBUG)

        logging.basicConfig(format="%(asctime)s [%(levelname)s] %(pathname)s [line: %(lineno)d]  %(message)s",
                            datefmt="%d-%m-%Y %H:%M:%S")

        # 自定义日志格式(Formatter), 实例化一个日志格式类
        fmt_str = '%(asctime)s [%(levelname)s] %(pathname)s [line: %(lineno)d]  %(message)s'
        formatter = logging.Formatter(fmt_str)

        # 实例化控制台渠道(StreamHandle)
        sh = logging.StreamHandler()
        # 设置渠道当中的日志显示格式
        sh.setFormatter(formatter)
        # 将渠道与日志收集器绑定起来
        self.addHandler(sh)
        sh.close()

    def out(self, logger_type: int, log_msg: str, *args, **kwargs) -> None:
        if self.isEnabledFor(logger_type):
            self._log(logger_type, log_msg, args, **kwargs)
