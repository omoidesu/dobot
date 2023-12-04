# dodo-sdk

一个专用于 [Dodo](https://www.imdodo.com/) 的Python SDK  
[Dodo开发者文档](https://open.imdodo.com/)

# 简单示例

```json
{
  "client_id": "xxxx",
  "token": "xxxxx"
}
```

```python
import json

from dobot import Bot
from dobot.eventMessage.msg import Msg

with open("bot.json", "r", encoding="utf-8") as f:
  bot_info = json.load(f)

# 初始化bot
bot = Bot(bot_info.get("client_id"), bot_info.get("token"))


# 这里开始你的业务逻辑，服务器中输入.ping 或 /ping即可跳转至对应方法
@bot.on_message("ping", prefix=['/', '.'], at_bot=False)
async def ping(msg: Msg):
  """
  业务主体
  """
  # 回复消息
  reply_message: Msg = await msg.reply("pong!")
  # 给回复的消息添加回应
  await reply_message.add_reaction("👍")
  # 移除表情
  await reply_message.remove_reaction("👍")
  # 修改消息
  await reply_message.edit("我现在不是pong了")
  # 置顶消息
  await reply_message.top()
  # 取消置顶
  await reply_message.cancel_top()
  # 撤回消息
  await reply_message.delete("我撤回了略略略")


# bot的运行方法
if __name__ == '__main__':
  bot.run()
```

# 环境

requirement: Python >= 3.7

不确定是否向下兼容

# 现有功能

### 仅支持频道消息Event - 消息事件

**频道消息API**：

- 发送消息： √
- 编辑消息： √
- 撤回消息： √
- 置顶消息：
    - 置顶消息： √
    - 取消置顶： √
- 获取消息反应列表： ×
- 获取消息反应内成员列表： ×
- 添加表情反应： √
- 取消表情反应： √

# 文档

暂无

# PS.

本项目一定程度上参考了[khl.py](https://github.com/TWT233/khl.py)和[Django](https://github.com/django/django)，khl.py的逻辑结构和django的实用方法都对本项目有很大的帮助！

另外，项目中有很多不完善/奇思妙想的代码，并且代码结构和逻辑结构都还不是很完善，欢迎大家提出建议和PR！

