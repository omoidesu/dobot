from abc import ABC, abstractmethod


class LogAbstractObject(ABC):
    @abstractmethod
    def time_logger_wrapper(self):
        ...

    @abstractmethod
    def async_time_logger_wrapper(self):
        ...
