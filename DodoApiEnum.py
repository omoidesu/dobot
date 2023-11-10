from enum import Enum


class DodoApiEnum(Enum):
    # API地址
    BASE_API_URL = "https://botopen.imdodo.com"

    # WS连接地址
    WS_CLIENT_GETTER_URL = "/api/v2/websocket/connection"
