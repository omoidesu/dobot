from datetime import datetime

import Logging
from Logging import MyLogger

logger = MyLogger()


def class_logger_wrapper(obj):
    """
    类装饰器，用于给类添加time_logger_wrapper和async_time_logger_wrapper方法
    :param obj: 被装饰的类
    :return:
    """

    def time_logger_wrapper(self, print_time_logger: bool = False):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = datetime.now()
                if print_time_logger:
                    logger.out(Logging.DEBUG,
                               f"Function: {func.__name__}, Args: {args}, kwargs: {kwargs}, StartTime: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                res = func(*args, **kwargs)
                end_time = datetime.now()
                sub_time = end_time - start_time
                if print_time_logger:
                    logger.out(Logging.DEBUG,
                               f"Function: {func.__name__}, Args: {args}, kwargs: {kwargs}, EndTime: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    logger.out(Logging.DEBUG,
                               f"Function: {func.__name__}, Args: {args}, kwargs: {kwargs}, ExecuteTime: {str(sub_time.total_seconds())}s")
                return res

            return wrapper

        return decorator

    def async_time_logger_wrapper(self, print_time_logger: bool = False):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = datetime.now()
                if print_time_logger:
                    logger.out(Logging.DEBUG,
                               f"Function: {func.__name__}, Args: {args}, kwargs: {kwargs}, StartTime: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                res = await func(*args, **kwargs)
                end_time = datetime.now()
                sub_time = end_time - start_time
                if print_time_logger:
                    logger.out(Logging.DEBUG,
                               f"Function: {func.__name__}, Args: {args}, kwargs: {kwargs}, EndTime: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    logger.out(Logging.DEBUG,
                               f"Function: {func.__name__}, Args: {args}, kwargs: {kwargs}, ExecuteTime: {str(sub_time.total_seconds())}s")
                return res

            return wrapper

        return decorator

    obj.time_logger_wrapper = time_logger_wrapper
    obj.async_time_logger_wrapper = async_time_logger_wrapper
    return obj
