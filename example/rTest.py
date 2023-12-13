import asyncio
import json

from dobot import Bot
from dobot.file.R import R
from dobot.file.file.image import Image

# 读取bot配置信息
with open("bot.json", "r", encoding="utf-8") as f:
  bot_info = json.load(f)

# 在同此文件路径下配置bot.json或初始化填入botId及token
# 初始化bot
bot = Bot(bot_info.get("client_id"), bot_info.get("token"))

r = R()

async def timed():
    # 这里把放置图片的路径放入R的监控列表中，后续文件有变动会直接调用底层预处理文件的方法
    await r.add_path(r"D:\PyCode\dodo.py\test1")
    res: Image = r.get_image(r"D:\PyCode\dodo.py\test1\123.jpg")
    print(await res.url)
    print(await res.height)
    print(await res.width)

async def main():
    await asyncio.gather(timed())

asyncio.run(main())