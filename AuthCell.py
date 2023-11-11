class AuthCell:
    """
    用于存储 Bot 的 ID 和 Token
    单例
    """
    _instance: 'AuthCell' = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, bot_id=None, bot_token=None):
        if not hasattr(self, 'initialized'):
            self.bot_id = bot_id
            self.bot_token = bot_token
            self.initialized = True

    @classmethod
    def get_instance(cls):
        return cls._instance
