import websocket, requests, json, time
import _thread as thread

from DodoApiEnum import DodoApiEnum
from logger import MyLogger


logger = MyLogger()

class BotClient:
    def __init__(self, bot_id: str, bot_token: str) -> None:
        self.__bot_id = bot_id
        self.__bot_token = bot_token
        self.__ws_url_dict = self.__get_ws_url()
        # 启动ws连接
        self.__ws_connect()

    @staticmethod
    def __ws_heart_beat(ws):
        def run(*args):
            while True:
                time.sleep(14) # ws要求30s的心跳相应，这里设置14s应对网络突发情况
                ws.send('{"type": 1}') # 心跳数据

        thread.start_new_thread(run, ())

    @staticmethod
    def __on_message(ws, message):
        msg_dict = json.loads(message)
        if msg_dict["type"] == 1:
            logger.debug("##### ws connection heart beat #####")
        else:
            logger.debug(bytes.decode(message))

    @staticmethod
    def __on_error(ws, error):
        logger.error("##### ws connection error #####")

    @staticmethod
    def __on_close(ws, close_status_code, close_message):
        logger.debug("##### ws connection closed #####")

    def __get_ws_url(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bot {self.__bot_id}.{self.__bot_token}"
        }
        res = requests.post(DodoApiEnum.BASE_API_URL.value, headers=headers)
        return json.loads(res.text)

    def __ws_connect(self):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(self.__ws_url_dict["data"]["endpoint"],
                                    on_message=self.__on_message,
                                    on_error=self.__on_error,
                                    on_close=self.__on_close)
        ws.on_open = self.__ws_heart_beat
        ws.run_forever()

if __name__ == "__main__":
    bot_client = BotClient("83199120", "ODMxOTkxMjA.77-9LAnvv70.4-jInox-uI8LTujPQZASLRGcxd_mn5twL-55m0LK7xc")