class Reference:
    def __init__(self, reference: dict):
        self._message_id = reference.get('messageId', '')
        self._dodo_source_id = reference.get('dodoSourceId', '')
        self._nick_name = reference.get('nickName', '')

    @property
    def message_id(self):
        return self._message_id

    @property
    def dodo_source_id(self):
        return self._dodo_source_id

    @property
    def nick_name(self):
        return self._nick_name