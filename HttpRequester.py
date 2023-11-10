from interface.LogAbstractObject import LogAbstractObject
from wrapper.ClassLoggerWrapper import ClassLoggerWrapper


@ClassLoggerWrapper
class HttpRequester(LogAbstractObject):
    _print_logger: bool = False

    def __init__(self, print_logger: bool = None):
        if print_logger is not None:
            self._print_logger = print_logger

    def time_logger_wrapper(self, print_logger: bool = False):
        def decorator(func):
            def wrapper(*args, **kwargs):
               pass

            return wrapper

        return decorator

    def async_time_logger_wrapper(self, print_logger: bool = False):
        def decorator(func):
            def wrapper(*args, **kwargs):
                pass

            return wrapper

        return decorator

    def request(self, method: str, route: str, **params):
        @self.time_logger_wrapper(self._print_logger)
        def request(method: str, route: str, **params):
            print("request")

        return request(method, route, **params)

if __name__ == "__main__":
    h = HttpRequester(True)
    h.request("1", "2", a=1, b=2)



