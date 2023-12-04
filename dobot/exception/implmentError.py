class ImplementError(Exception):
    _class_name: str
    _method_name: str

    def __init__(self, class_name: str, method_name: str):
        super().__init__()
        self._class_name = class_name
        self._method_name = method_name

    def __str__(self):
        return f"Class '{self._class_name}' don't have method '{self._method_name}'"
