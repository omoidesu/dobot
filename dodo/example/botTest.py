import json

from dodo import Bot
from dodo.eventMessage.msg import Msg
from dodo.interface.message import Message

with open("bot.json", "r", encoding="utf-8") as f:
    bot_info = json.load(f)

# 初始化bot
bot = Bot(bot_info.get("client_id"), bot_info.get("token"))


# 在这里你只需要专注你的业务而无需考虑和Dodo通信的问题
@bot.on_message("ping", prefix=['/', '.', ','], at_bot=False)
async def ping(msg: Msg):
    # print("我是业务方法")
    # at成员id
    # print(msg.body.content_info.__dict__())
    # 回复消息
    reply_message: Msg = await msg.reply("pong!")
    # 给回复的消息添加回应
    # await reply_message.add_reaction("👍")


# bot的运行方法
if __name__ == '__main__':
    bot.run()
