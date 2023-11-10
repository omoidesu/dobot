import websockets, requests, json, time, asyncio

from DodoApiEnum import DodoApiEnum
from interface.AsyncRegisterObject import AsyncRegisterObject
from logger import MyLogger

logger = MyLogger()


class BotClient(AsyncRegisterObject):
    def __init__(self, bot_id: str, bot_token: str) -> None:
        self.__bot_id: str = bot_id
        self.__bot_token: str = bot_token
        self.__ws_url_dict: dict = {}

    @staticmethod
    async def _ws_heart_beat(ws):
        while True:
            await asyncio.sleep(14)  # ws要求30s的心跳相应，这里设置14s应对网络突发情况
            await ws.send('{"type": 1}')  # 心跳数据

    @staticmethod
    async def _receive_ws_msg(ws):
        while True:
            recv_text = await ws.recv()
            msg_dict = json.loads(recv_text)
            if msg_dict["type"] == 1:
                logger.debug("##### ws connection heart beat #####")
            else:
                logger.debug(f"服务器接收信息: {bytes.decode(recv_text)}")

    def __get_ws_url(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bot {self.__bot_id}.{self.__bot_token}"
        }
        res = requests.post(DodoApiEnum.BASE_API_URL.value + DodoApiEnum.WS_CLIENT_GETTER_URL.value, headers=headers)
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
