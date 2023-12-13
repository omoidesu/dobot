import json

# bot主类
from dobot import Bot
# 服务器返回消息解析后的Msg类，内含消息类型API的封装方法
from dobot import Msg
from dobot.const import EventType
from dobot.file.R import R
from dobot.file.file.image import Image

# 读取bot配置信息
with open("bot.json", "r", encoding="utf-8") as f:
  bot_info = json.load(f)

# 在同此文件路径下配置bot.json或初始化填入botId及token
# 初始化bot
bot = Bot(bot_info.get("client_id"), bot_info.get("token"))


# 这里开始你的业务逻辑，服务器中输入.ping 或 /ping即可跳转至对应方法
@bot.on_message("ping", prefix=['/', '.'], at_bot=False)
async def ping(msg: Msg):
  """
  业务主体
  """
  # # 回复消息
  # reply_message: Msg = await msg.reply("pong!")
  # # 给回复的消息添加回应
  # await reply_message.add_reaction("👍")
  # # 移除表情
  # await reply_message.remove_reaction("👍")
  # # 修改消息
  # await reply_message.edit("我现在不是pong了")
  # # 置顶消息
  # await reply_message.top()
  # # 取消置顶
  # await reply_message.cancel_top()
  # # 撤回消息
  # await reply_message.delete("我撤回了略略略")
  r = R()
  await r.add_path(r"D:\PyCode\dodo.py\test1")
  res: Image = r.get_image(r"D:\PyCode\dodo.py\test1\111.png")
  await msg.send(res)

@bot.on_event(event_type=EventType.EMOJI_REACTION)
async def on_ready(msg: Msg):
  await msg.send("谁让你给我表情反应了", at_sender=True)


# bot的运行方法
if __name__ == '__main__':
  bot.run()