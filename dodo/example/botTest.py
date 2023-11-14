import json

from dodo import Bot
from dodo.interface.message import Message

with open("bot.json", "r", encoding="utf-8") as f:
    bot_info = json.load(f)

# 初始化bot
bot = Bot(bot_info.get("client_id"), bot_info.get("token"))


# 在这里你只需要专注你的业务而无需考虑和Dodo通信的问题
@bot.on_message("ping", prefix=['/', '.', ','])
async def ping(msg: Message):
    print("我是业务方法")
    reply_message: Message = await msg.reply("pong!")
    await reply_message.add_reaction("👍")


# bot的运行方法
if __name__ == '__main__':
    bot.run()
