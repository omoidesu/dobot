class AuthCell:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
            return instance
        else:
            return cls._instances[cls]

    def __init__(self, bot_id=None, bot_token=None):
        if not hasattr(self, 'initialized'):
            self.bot_id = bot_id
            self.bot_token = bot_token
            self.initialized = True
