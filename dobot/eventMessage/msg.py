from typing import Union

from dobot.cert import AuthInfo
from dobot.const import MessageType
from dobot.eventMessage.message.baseMsg import BaseMsg
from dobot.eventMessage.message.cardMsg import CardMsg
from dobot.eventMessage.message.component.channal import Channel
from dobot.eventMessage.message.component.island import Island
from dobot.eventMessage.message.component.member import Member
from dobot.eventMessage.message.component.personal import Personal
from dobot.eventMessage.message.component.reference import Reference
from dobot.eventMessage.message.component.user import User
from dobot.eventMessage.message.context import Context
from dobot.eventMessage.message.fileMsg import FileMsg
from dobot.eventMessage.message.imageMsg import ImageMsg
from dobot.eventMessage.message.publicMsg import PublicMsg
from dobot.eventMessage.message.redPacketMsg import RedPacketMsg
from dobot.eventMessage.message.shareMsg import ShareMsg
from dobot.eventMessage.message.videoMsg import VideoMsg
from dobot.file.file.image import Image
from dobot.functional import CachedClass


class Msg:
    """
    内置属性：
        这部分的内容是类中自带的属性，直接用类的实例 + . + 属性名 即可获取，根据事件消息的不同可能个别属性没有值
        island_source_id: 群Id
        channel_id: 频道Id
        dodo_source_id: 消息发送人ID
        message_id: 消息ID
        personal: 消息发送人信息
            nick_name: 发送人名称
            avatar_url: 发送人头像
            sex: 发送人性别 -1：保密，0：女，1：男
        member: 消息发送人群内信息
            nick_name: 发送人名称
            join_time: 发送人加入群时间
        reference: 消息引用信息
            messageId: 引用消息ID
            dodoSourceId: 引用消息发送人ID
            nickName: 引用消息发送人名称
        messageType: 消息类型
        massageBody: 消息主体
            具体内容查看message文件夹对应类型.py文件

        mention: 获取消息里面的的@信息
        pre_mention: 获取消息指令之前的@信息 比如 @bot .ping 返回的是被@的bot的ID

    内置方法：
        send: 发送消息
        reply: 回复消息
        edit: 编辑消息
        delete: 撤回消息
        top: 置顶消息
        cancel_top: 取消置顶
        add_reaction: 给消息添加表情反应
        remove_reaction: 移除消息的表情反应
    """

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
            return BaseMsg()

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

    async def send(self,
                   content: Union[str, BaseMsg, Image, CachedClass],
                   at_sender: bool = False):
        if at_sender:
            content = f"<@!{self.dodo_source_id}> {content}" if isinstance(content, str) else content
        if isinstance(content, Image):
            content: Image
            content: BaseMsg = ImageMsg(url=await content.url, height=await content.height, width=await content.width)
        res: dict = await self.body.send(content)
        _event_body = res.get('data', {})
        _event_body['messageType'] = MessageType.TEXT.value if isinstance(content, str) else content._MESSAGE_TYPE
        _event_body['channelId'] = self.ctx.channel.id
        _event_body['islandSourceId'] = self.ctx.island.id
        _event_body['dodoSourceId'] = AuthInfo.get_instance().me

        return Msg(_event_body)

    async def reply(self,
                    content: Union[str, BaseMsg, Image, CachedClass],
                    at_sender: bool = False):
        if at_sender:
            content = f"<@!{self.dodo_source_id}> {content}" if isinstance(content, str) else content
        if isinstance(content, Image):
            content: Image
            content: BaseMsg = ImageMsg(url=await content.url, height=await content.height, width=await content.width)
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

    async def top(self):
        return await self.body.top()

    async def cancel_top(self):
        return await self.body.cancel_top()

    async def add_reaction(self, emoji: str):
        return await self.body.add_reaction(emoji)

    async def remove_reaction(self, emoji: str):
        return await self.body.remove_reaction(emoji)
