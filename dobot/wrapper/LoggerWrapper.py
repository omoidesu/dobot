from datetime import datetime

from dobot import log
from dobot.log import MyLogger

logger = MyLogger()


def time_logger_wrapper(print_time_logger: bool = False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            if print_time_logger:
                logger.out(log.DEBUG,
                           f"Function: {func.__name__}, Args: {args}, StartTime: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            res = func(*args, **kwargs)
            end_time = datetime.now()
            sub_time = end_time - start_time
            if print_time_logger:
                logger.out(log.DEBUG,
                           f"Function: {func.__name__}, Args: {args}, EndTime: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
                logger.out(log.DEBUG,
                           f"Function: {func.__name__}, Args: {args}, ExecuteTime: {str(sub_time.total_seconds())}s")
            return res

        return wrapper

    return decorator


def async_time_logger_wrapper(print_time_logger: bool = False):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = datetime.now()
            if print_time_logger:
                logger.out(log.DEBUG,
                           f"Function: {func.__name__}, Args: {args}, StartTime: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            res = await func(*args, **kwargs)
            end_time = datetime.now()
            sub_time = end_time - start_time
            if print_time_logger:
                logger.out(log.DEBUG,
                           f"Function: {func.__name__}, Args: {args}, EndTime: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
                logger.out(log.DEBUG,
                           f"Function: {func.__name__}, Args: {args}, ExecuteTime: {str(sub_time.total_seconds())}s")
            return res

        return wrapper

    return decorator
