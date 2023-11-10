import _thread as thread
import asyncio
import json
import time

import requests
import websockets


# 获取websocket连接

def get_ws_url() -> dict:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bot 83199120.ODMxOTkxMjA.77-9LAnvv70.4-jInox-uI8LTujPQZASLRGcxd_mn5twL-55m0LK7xc"
    }
    res = requests.post("https://botopen.imdodo.com/api/v2/websocket/connection", headers=headers)
    return json.loads(res.text)


res_dict = get_ws_url()
print(res_dict)


def on_open(ws):
    def run(*args):
        while True:
            time.sleep(14)
            ws.send('{"type": 1}')

    thread.start_new_thread(run, ())


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close):
    print(close)


# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp(res_dict["data"]["endpoint"],
#                               on_message = on_message,
#                               on_error = on_error,
#                               on_close = on_close)
#     ws.on_open = on_open
#     ws.run_forever()

async def _ws_heart_beat(ws):
    while True:
        await asyncio.sleep(1)  # ws要求30s的心跳相应，这里设置14s应对网络突发情况
        await ws.send('{"type": 1}')  # 心跳数据


async def _receive_ws_msg(ws):
    while True:
        print("准备接收信息")
        recv_text = await ws.recv()
        print(recv_text)


async def hello(res_dict):
    async for websocket in websockets.connect(res_dict["data"]["endpoint"], ping_interval=None):
        try:
            await asyncio.gather(_ws_heart_beat(websocket), _receive_ws_msg(websocket))
        except websockets.ConnectionClosed:
            print("ws连接中断，正在重新连接")
            continue


asyncio.get_event_loop().run_until_complete(
    hello(res_dict))
