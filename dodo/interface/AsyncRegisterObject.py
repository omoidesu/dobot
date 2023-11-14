from abc import ABC, abstractmethod
import asyncio


class AsyncRegisterObject(ABC):
    _loop: asyncio.AbstractEventLoop = None

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @loop.setter
    def loop(self, new_loop: asyncio.AbstractEventLoop):
        self._loop = new_loop

    @abstractmethod
    def run(self, *args, **kwargs):
        ...
