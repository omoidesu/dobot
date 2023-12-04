import json
import time

from dodo import Bot
from dodo.eventMessage.msg import Msg

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
    await reply_message.add_reaction("👍")
    time.sleep(2)
    await reply_message.remove_reaction("👍")
    # time.sleep(2)
    # await reply_message.edit("我现在不是pong了")
    # time.sleep(2)
    # await reply_message.delete("我撤回了略略略")
    # time.sleep(2)
    # await reply_message.top()
    # time.sleep(2)
    # await reply_message.cancel_top()


# bot的运行方法
if __name__ == '__main__':
    bot.run()
