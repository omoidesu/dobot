import asyncio

from dobot.file.R import R
from dobot.file.monitor.baseFileMonitor import BaseFileMonitor

r = R()

async def timed():
    # 这里把放置图片的路径放入R的监控列表中，后续文件有变动会直接调用底层预处理文件的方法
    await r.add_path(r"D:\PyCode\dodo.py\test1")
    while True:
        # 验证监控路径本身是异步非阻塞的，拿一个定时器来验证
        print("123")
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(timed())

asyncio.run(main())