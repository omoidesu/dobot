from dodo import Bot
from dodo.interface.message import Message

# 初始化bot
bot = Bot("bot_id", "bot_token")

# 在这里你只需要专注你的业务而无需考虑和Dodo通信的问题
@bot.on_message("info", prefix=['/', '.', ','])
async def func1(msg: Message):
    print("我是业务方法")

# bot的运行方法
if __name__ == '__main__':
    bot.run()