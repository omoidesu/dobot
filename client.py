import asyncio
import json
import time
import websockets
import websocket
import requests
try:
    import thread
except ImportError:
    import _thread as thread

# 获取websocket连接

def get_ws_url() -> dict:
    URL = "https://botopen.imdodo.com/api/v2/websocket/connection"
    HEADERS = {
       "Content-Type": "application/json",
       "Authorization": "Bot.py 83199120.ODMxOTkxMjA.77-9LAnvv70.4-jInox-uI8LTujPQZASLRGcxd_mn5twL-55m0LK7xc"
    }
    res = requests.post(URL, headers=HEADERS)
    print(json.loads(res.text))
    return json.loads(res.text)

res_dict = get_ws_url()

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


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(res_dict["data"]["endpoint"],
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()


# async def hello(res_dict):
#     async with websockets.connect(res_dict["data"]["endpoint"]) as websocket:
#         await websocket.send('{"type": 1}')
#         recv_text = await websocket.recv()
#         print(recv_text)


# asyncio.get_event_loop().run_until_complete(
#     hello(res_dict))