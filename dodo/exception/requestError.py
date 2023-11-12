class RequestError(Exception):
    _status_code: int
    _route: str

    def __init__(self, status_code: int, route: str):
        super().__init__()
        self._status_code = status_code
        self._route = route

    def __str__(self):
        return f"Requesting '{self._route}' failed with http_code {self._status_code}"


class ApiRequestError(RequestError):
    _params: dict
    _status: int
    _message: str

    def __init__(self, status_code: int, route: str, params: dict, status: int, message: str):
        super().__init__(status_code, route)
        self._params = params
        self._status = status
        self._message = message

    def __str__(self):
        return f"Requesting '{self._route}' failed with {self._status}: {self._message}"
