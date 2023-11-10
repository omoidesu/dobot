import Logging
from Logging import MyLogger

logger = MyLogger()


def ClassLoggerWrapper(obj):
    def time_logger_wrapper(self, print_logger: bool = False):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if print_logger:
                    logger.out(Logging.DEBUG, f"Function: {func.__name__}, Args: {args}, kwargs: {kwargs}")
                res = func(*args, **kwargs)
                if print_logger:
                    logger.out(Logging.DEBUG, f"Function: {func.__name__}, Args: {args}, kwargs: {kwargs}")
                return res

            return wrapper

        return decorator

    def async_time_logger_wrapper(self, print_logger: bool = False):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                if print_logger:
                    logger.out(Logging.DEBUG, f"func: {func.__name__} args: {args} kwargs: {kwargs}")
                res = await func(*args, **kwargs)
                if print_logger:
                    logger.out(Logging.DEBUG, f"func: {func.__name__} args: {args} kwargs: {kwargs}")
                return res

            return wrapper

        return decorator

    obj.time_logger_wrapper = time_logger_wrapper
    obj.async_time_logger_wrapper = async_time_logger_wrapper
    return obj
