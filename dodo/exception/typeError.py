class _TypeError(Exception):
    _allow_types: list

    def __init__(self, allow_types: list):
        super().__init__()
        if not isinstance(allow_types, list):
            raise TypeError("allow_types must be a list")

        if len(allow_types) == 0:
            raise ValueError("allow_types must not be empty")

        self._allow_types = allow_types


class MessageTypeError(_TypeError):
    def __init__(self, allow_type: list, message_type: int = 0):
        if not message_type:
            super().__init__(allow_type)
        else:
            self.message_type = message_type

    def __str__(self):
        if self.message_type:
            return f"messageType must be {self.message_type}"
        else:
            return f"messageType must be in {self._allow_types}"
