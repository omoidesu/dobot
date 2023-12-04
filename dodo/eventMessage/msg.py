from typing import Union

from dodo.cert import AuthInfo
from dodo.const import SUCCESS, MessageType
from dodo.eventMessage.message.component.channal import Channel
from dodo.eventMessage.message.component.island import Island
from dodo.eventMessage.message.component.member import Member
from dodo.eventMessage.message.baseMsg import BaseMsg
from dodo.eventMessage.message.cardMsg import CardMsg
from dodo.eventMessage.message.component.user import User
from dodo.eventMessage.message.fileMsg import FileMsg
from dodo.eventMessage.message.imageMsg import ImageMsg
from dodo.eventMessage.message.publicMsg import PublicMsg
from dodo.eventMessage.message.redPacketMsg import RedPacketMsg
from dodo.eventMessage.message.shareMsg import ShareMsg
from dodo.eventMessage.message.videoMsg import VideoMsg
from dodo.eventMessage.message.component.personal import Personal
from dodo.eventMessage.message.component.reference import Reference
from dodo.messagebak.context import Context


class Msg:

    @staticmethod
    def parseMsg(message_type: int, event_body: dict) -> BaseMsg:
        if message_type == 1:
            return PublicMsg(event_body.get('messageBody', {}))
        elif message_type == 2:
            return ImageMsg(event_body.get('messageBody', {}))
        elif message_type == 3:
            return VideoMsg(event_body.get('messageBody', {}))
        elif message_type == 4:
            return ShareMsg(event_body.get('messageBody', {}))
        elif message_type == 5:
            return FileMsg(event_body.get('messageBody', {}))
        elif message_type == 6:
            return CardMsg(event_body.get('messageBody', {}))
        elif message_type == 7:
            return RedPacketMsg(event_body.get('messageBody', {}))
        else:
            raise ValueError(f"Invalid Message Type! need 1-7 but {message_type} was given")

    def __init__(self, event_body: dict):
        """
        存放msg的主体类，包含所有msg相关信息
        如果想查看具体msg的请求方式，请查看对应消息类型的msg，例如图片消息查看ImageMsg的类方法
        """
        self.island_source_id = event_body.get('islandSourceId', '')
        self.channel_id = event_body.get('channelId', '')
        self.dodo_source_id = event_body.get('dodoSourceId', '')
        self.message_id = event_body.get('messageId', '')
        self.message_type = event_body.get('messageType', '')

        # personal
        self.personal = Personal(event_body.get('personal', {}))

        # member
        self.member = Member(event_body.get('member', {}))

        # reference
        self.reference = Reference(event_body.get('reference', {}))

        # msg
        self.body = self.parseMsg(self.message_type, event_body)

        # context
        __user = User(
            id=self.dodo_source_id,
            personal_nickname=self.personal.nick_name,
            avatar=self.personal.avatar_url,
            sex=self.personal.sex,
            island_id=self.island_source_id,
            nickname=self.member.nick_name,
            joined_at=self.member.join_time
        )
        __channel = Channel(id=self.channel_id)
        __island = Island(id=self.island_source_id)
        self.ctx = Context(__island, __channel, __user)

        # 将上下文传递到body中等待msg调用
        self.body.ctx = self.ctx
        self.body.message_id = self.message_id

    @property
    def mention(self):
        """
        获取消息的@信息
        """
        return self.body.mention

    @property
    def pre_mention(self):
        """
        获取消息prefix之前的@信息
        """
        return self.body.pre_mention

    async def reply(self, content: Union[str, BaseMsg]):
        res: dict = await self.body.reply(content)
        _event_body = res.get('data', {})
        _event_body['messageType'] = MessageType.TEXT.value if isinstance(content, str) else content._MESSAGE_TYPE
        _event_body['channelId'] = self.ctx.channel.id
        _event_body['islandSourceId'] = self.ctx.island.id
        _event_body['dodoSourceId'] = AuthInfo.get_instance().me

        return Msg(_event_body)

    async def edit(self, content: Union[str, BaseMsg]):
        res: dict = await self.body.edit(content)
        _event_body = res.get('data', {})
        _event_body['messageType'] = MessageType.TEXT.value if isinstance(content, str) else content._MESSAGE_TYPE
        _event_body['channelId'] = self.ctx.channel.id
        _event_body['islandSourceId'] = self.ctx.island.id
        _event_body['dodoSourceId'] = AuthInfo.get_instance().me

        return Msg(_event_body)

    async def delete(self, reason: str, message_id: str = None):
        return await self.body.delete(reason, message_id)

    async def add_reaction(self, emoji: str):
        return await self.body.add_reaction(emoji)


if __name__ == "__main__":
    event_body = {
        "islandSourceId": "44659",
        "channelId": "118506",
        "dodoSourceId": "681856",
        "messageId": "349552072708214784",
        "personal": {
            "nickName": "测试DoDo昵称",
            "avatarUrl": "https://static.imdodo.com/DoDoRes/Avatar/6.png",
            "sex": 1
        },
        "member": {
            "nickName": "测试群昵称",
            "joinTime": "2022-07-20 10:27:24"
        },
        "reference": {
            "messageId": "",
            "dodoSourceId": "",
            "nickName": ""
        },
        "messageType": 1,
        "messageBody": {
            "content": "<@!3946846> .ping"
        }
    }
    m = Msg(event_body)
    print(m.mention)
