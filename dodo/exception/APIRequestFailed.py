class APIRequestFailed(Exception):
    """
    This class is copied from khl.py /khl/requester.py
    """

    def __init__(self, method, route, params, err_code, err_message):
        super().__init__()
        self.method = method
        self.route = route
        self.params = params
        self.err_code = err_code
        self.err_message = err_message

    def __str__(self):
        return f"Requesting '{self.method} {self.route}' failed with {self.err_code}: {self.err_message}"
