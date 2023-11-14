import asyncio
import json

import requests
import websockets

from .cert import AuthCell
from .const import Route
from .handler import EventHandler
from .log import MyLogger
from .interface.AsyncRegisterObject import AsyncRegisterObject

logger = MyLogger()


class BotClient(AsyncRegisterObject):
    """
    websocket客户端
    """

    def __init__(self, handler: EventHandler) -> None:
        self.__auth_cell = AuthCell.get_instance()
        self.__handler: EventHandler = handler
        self.__bot_id: str = self.__auth_cell.bot_id
        self.__bot_token: str = self.__auth_cell.bot_token
        self.__ws_url_dict: dict = {}

    def _parser_receive_msg(self, msg: dict):
        self.__handler._handle_msg(msg)

    @staticmethod
    async def _ws_heart_beat(ws):
        while True:
            await asyncio.sleep(14)  # ws要求30s的心跳相应，这里设置14s应对网络突发情况
            await ws.send('{"type": 1}')  # 心跳数据

    async def _receive_ws_msg(self, ws):
        while True:
            recv_text = await ws.recv()
            msg_dict = json.loads(recv_text)
            if msg_dict["type"] == 1:
                logger.debug("##### ws connection heart beat #####")
            else:
                logger.debug(f"服务器接收信息: {msg_dict}")
                self._parser_receive_msg(msg_dict)

    def __get_ws_url(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bot {self.__bot_id}.{self.__bot_token}"
        }
        res = requests.post(Route.GET_WEBSOCKET_CONNECTION.value, headers=headers)
        return res.json()

    async def __ws_connect(self):
        async for websocket in websockets.connect(self.__ws_url_dict["data"]["endpoint"],
                                                  ping_interval=None,
                                                  logger=None):
            try:
                await asyncio.gather(self._ws_heart_beat(websocket), self._receive_ws_msg(websocket))
            except websockets.ConnectionClosed:
                logger.error("ws连接中断，正在重新连接")
                continue

    def run(self):
        self.__ws_url_dict = self.__get_ws_url()
        if not self._loop:
            self._loop = asyncio.get_event_loop()
        self._loop.run_until_complete(self.__ws_connect())
