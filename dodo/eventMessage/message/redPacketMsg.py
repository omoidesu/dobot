from dodo.const import MessageType
from dodo.eventMessage.message.baseMsg import BaseMsg
from dodo.eventMessage.message.context import Context


class RedPacketMsg(BaseMsg):
    _MESSAGE_TYPE = MessageType.RED_PACKET.value
    _ctx: Context
    def __init__(self, message_body: dict):
        self._type = message_body.get('type', 0)
        self._count = message_body.get('count', 0)
        self._total_amount = message_body.get('totalAmount', 0)
        self._receiver_type = message_body.get('receiverType', 0)
        self._role_id_list = message_body.get('roleIdList', [])

    @property
    def type(self):
        return self._type

    @property
    def count(self):
        return self._count

    @property
    def total_amount(self):
        return self._total_amount

    @property
    def receiver_type(self):
        return self._receiver_type

    @property
    def role_id_list(self):
        return self._role_id_list