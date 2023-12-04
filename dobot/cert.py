class AuthInfo:
    """
    用于存储 Bot 的 ID 和 Token
    单例
    """
    _initialized: bool = False
    _instance: 'AuthInfo' = None
    _header: dict = {"Content-Type": "application/json"}
    _bot_id: str = ""

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, bot_id=None, bot_token=None):
        if not hasattr(self, 'initialized'):
            self.bot_id = bot_id
            self.bot_token = bot_token
            self.initialized = True
            self._header['Authorization'] = f'Bot {self.bot_id}.{self.bot_token}'

    @classmethod
    def get_instance(cls):
        return cls._instance

    @property
    def header(self):
        return self._header

    @property
    def me(self):
        return self._bot_id

    @me.setter
    def me(self, bot_id: str):
        self._bot_id = bot_id
