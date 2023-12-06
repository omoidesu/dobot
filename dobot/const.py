from enum import Enum

SUCCESS = 0

# 系统内核
WINDOWS = 0
LINUX = 1

PICTURE_SUFFIX = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']

FILE_CREATED = 1
FILE_MODIFIED = 2
FILE_DELETED = 3
FILE_RENAMED = 4
FILE_UNKNOWN = 32768

# 返回码
RESPONSE_STATUS_CODE = {
    0: '成功',
    -9999: '系统异常',
    10000: '请求参数非法',
    10001: '鉴权clientId或者token 两个字段都不能为空',
    10002: '请求参数不能为空',
    10003: '不是成员',
    10004: '没有mqtt服务连接点',
    10005: '鉴权失败',
    10006: '修改昵称用户不属于你的群',
    10007: '机器人被封禁',
    10008: 'clientId不存在',
    10009: '群不存在',
    10010: '频道不存在',
    10011: '只允许在文字频道发送消息',
    10012: '验证签名timestamp字段不能为空',
    10013: '验证签名sign字段不能为空',
    10014: '签名url过期',
    10015: '签名失败',
    10016: '只允许发送域名包含imdodo.com的资源',
    10017: '用户不存在',
    10018: '消息不存在',
    10019: '文字内容校验异常',
    10020: '昵称长度不能超过32字符',
    10021: '介绍长度不能超过200字符',
    10022: '记录已存在,请勿重复操作',
    10023: '机器人创建数量上限为20，你已达到创建数量上限',
    10024: '机器人调用太频繁，触发限流',
    10025: '无权限操作',
    10026: '系统负载过高，请稍后重试',
    10027: '账号不存在',
    10028: '开发者未被认证，不能创建机器人',
    10029: '开发者被封禁中',
    10030: '手机号非法',
    10031: '验证码发送频繁，请稍后再试',
    10032: '机器人不能被邀请',
    10033: '机器人不存在',
    10034: '验证码已过期',
    10035: '验证码错误',
    10036: '登录token不能为空',
    10037: '登录token已过期',
    10038: '登录token非法',
    10039: '您今日邀请用户数已达上限（20个），请明日再试',
    10042: '暂未开放机器人@所有人功能',
    10043: '业务签名失败',
    10044: '暂未开放机器人@身份组功能',
    10045: '您的账号已被注销',
    10082: '该群已被限制发言频率处罚，1分钟内仅可发送一条消息',
    10083: '该群已被限制发言频率处罚，1分钟内仅可编辑一条消息',
    10084: '当前群未开通邀请系统',
    10085: '当前用户未绑定高能链钱包或未开启数字藏品展示',
    10086: '模版机器人不允许操作',
    10087: '未开通群等级',
    10088: '用户未开启数字藏品展示',
    10089: '权限值非法',
    10090: '组不存在',
    10091: '权限值有误，请检查操作身份组时允许的权限',
    10092: '系统维护中，暂不支持修改',
    10093: '系统维护中，暂不支持修改',
    10094: '系统维护中，暂时无法发布内容',
    10095: '系统维护中，暂不支持修改',
    10096: '帖子不存在',
    10097: '帖子已被删除',
    10099: '本群未开启赠礼系统',
    10100: '该类型消息不允许置顶',
    10101: '消息已处于置顶状态',
    10102: '该群开通了隐私保护模式，且您没有管理成员或超级管理员权限',
    10103: '对方不是该群成员',
    10104: '本群未开启积分系统'
}

# 文字消息中at成员的正则表达式
MENTION_PATTERN = r"<@!(\d+)>"


class Route(Enum):
    # API地址
    __BASE_API_URL = "https://botopen.imdodo.com/api/v2"

    """机器人API"""
    # 获取机器人信息
    GET_BOT_INFO = f"{__BASE_API_URL}/bot/info"
    # 机器人退群
    SET_BOT_ISLAND_LEAVE = f"{__BASE_API_URL}/bot/island/leave"
    # 获取机器人邀请列表
    GET_BOT_INVITE_LIST = f"{__BASE_API_URL}/bot/invite/list"
    # 添加成员到机器人邀请列表
    SET_BOT_INVITE_ADD = f"{__BASE_API_URL}/bot/invite/add"
    # 移除成员出机器人邀请列表
    SET_BOT_INVITE_REMOVE = f"{__BASE_API_URL}/bot/invite/remove"

    """群API"""
    # 获取群列表
    GET_ISLAND_LIST = f"{__BASE_API_URL}/island/list"
    # 获取群信息
    GET_ISLAND_INFO = f"{__BASE_API_URL}/island/info"
    # 获取群等级排行榜
    GET_ISLAND_LEVEL_RANK_LIST = f"{__BASE_API_URL}/island/level/rank/list"
    # 获取群禁言名单
    GET_ISLAND_MUTE_LIST = f"{__BASE_API_URL}/island/mute/list"
    # 获取群封禁名单
    GET_ISLAND_BAN_LIST = f"{__BASE_API_URL}/island/ban/list"

    """频道API"""
    # 获取频道列表
    GET_CHANNEL_LIST = f"{__BASE_API_URL}/channel/list"
    # 获取频道信息
    GET_CHANNEL_INFO = f"{__BASE_API_URL}/channel/info"
    # 创建频道
    SET_CHANNEL_ADD = f"{__BASE_API_URL}/channel/add"
    # 编辑频道
    SET_CHANNEL_EDIT = f"{__BASE_API_URL}/channel/edit"
    # 删除频道
    SET_CHANNEL_REMOVE = f"{__BASE_API_URL}/channel/remove"

    """频道消息API"""
    # 发送消息
    SET_CHANNEL_MESSAGE_SEND = f"{__BASE_API_URL}/channel/message/send"
    # 编辑消息
    SET_CHANNEL_MESSAGE_EDIT = f"{__BASE_API_URL}/channel/message/edit"
    # 撤回消息
    SET_CHANNEL_MESSAGE_WITHDRAW = f"{__BASE_API_URL}/channel/message/withdraw"
    # 置顶消息
    SET_CHANNEL_MESSAGE_TOP = f"{__BASE_API_URL}/channel/message/top"
    # 获取消息反应列表
    GET_CHANNEL_MESSAGE_REACTION_LIST = f"{__BASE_API_URL}/channel/message/reaction/list"
    # 获取消息反应内成员列表
    GET_CHANNEL_MESSAGE_REACTION_MEMBER_LIST = f"{__BASE_API_URL}/channel/message/reaction/member/list"
    # 添加表情反应
    SET_CHANNEL_MESSAGE_REACTION_ADD = f"{__BASE_API_URL}/channel/message/reaction/add"
    # 取消表情反应
    SET_CHANNEL_MESSAGE_REACTION_REMOVE = f"{__BASE_API_URL}/channel/message/reaction/remove"

    """语音频道API"""
    # 获取成员语音频道状态
    GET_CHANNEL_VOICE_MEMBER_STATUS = f"{__BASE_API_URL}/channel/voice/member/status"
    # 移动语音频道成员
    SET_CHANNEL_VOICE_MEMBER_MOVE = f"{__BASE_API_URL}/channel/voice/member/move"
    # 管理语音中的成员
    SET_CHANNEL_VOICE_MEMBER_EDIT = f"{__BASE_API_URL}/channel/voice/member/edit"

    """帖子频道API"""
    # 发布帖子
    SET_CHANNEL_ARTICLE_ADD = f"{__BASE_API_URL}/channel/article/add"
    # 删除帖子评论回复
    SET_CHANNEL_ARTICLE_REMOVE = f"{__BASE_API_URL}/channel/article/remove"

    """身分组API"""
    # 获取身分组列表
    GET_ROLE_LIST = f"{__BASE_API_URL}/role/list"
    # 创建身分组
    SET_ROLE_ADD = f"{__BASE_API_URL}/role/add"
    # 编辑身分组
    SET_ROLE_EDIT = f"{__BASE_API_URL}/role/edit"
    # 删除身分组
    SET_ROLE_REMOVE = f"{__BASE_API_URL}/role/remove"
    # 获取身分组成员列表
    GET_ROLE_MEMBER_LIST = f"{__BASE_API_URL}/role/member/list"
    # 赋予成员身分组
    SET_ROLE_MEMBER_ADD = f"{__BASE_API_URL}/role/member/add"
    # 取消成员身分组
    SET_ROLE_MEMBER_REMOVE = f"{__BASE_API_URL}/role/member/remove"

    """成员API"""
    # 获取成员列表
    GET_MEMBER_LIST = f"{__BASE_API_URL}/member/list"
    # 获取成员信息
    GET_MEMBER_INFO = f"{__BASE_API_URL}/member/info"
    # 获取成员身分组列表
    GET_MEMBER_ROLE_LIST = f"{__BASE_API_URL}/member/role/list"
    # 获取成员邀请信息
    GET_MEMBER_INVITATION_INFO = f"{__BASE_API_URL}/member/invitation/info"
    # 编辑成员群昵称
    SET_MEMBER_NICKNAME_EDIT = f"{__BASE_API_URL}/member/nickname/edit"
    # 禁言成员
    SET_MEMBER_MUTE_ADD = f"{__BASE_API_URL}/member/mute/add"
    # 取消成员禁言
    SET_MEMBER_MUTE_REMOVE = f"{__BASE_API_URL}/member/mute/remove"
    # 永久封禁成员
    SET_MEMBER_BAN_ADD = f"{__BASE_API_URL}/member/ban/add"
    # 取消成员永久封禁
    SET_MEMBER_BAN_REMOVE = f"{__BASE_API_URL}/member/ban/remove"

    """赠礼系统API"""
    # 获取群收入
    GET_GIFT_ACCOUNT = f"{__BASE_API_URL}/gift/account/info"
    # 获取成员分成管理
    GET_GIFT_SHARE_RATIO_INFO = f"{__BASE_API_URL}/gift/share/ratio/info"
    # 获取内容礼物列表
    GET_GIFT_LIST = f"{__BASE_API_URL}/gift/list"
    # 获取内容礼物内成员列表
    GET_GIFT_MEMBER_LIST = f"{__BASE_API_URL}/gift/member/list"
    # 获取内容礼物总值列表
    GET_GIFT_GROSS_VALUE_LISt = f"{__BASE_API_URL}/gift/gross/value/list"

    """积分系统API"""
    # 查询成员积分
    GET_INTEGRAL_INFO = f"{__BASE_API_URL}/integral/info"
    # 管理成员积分
    SET_INTEGRAL_EDIT = f"{__BASE_API_URL}/integral/edit"

    """私信API"""
    # 发送私信
    SET_PERSOINAL_MESSAGE_SEND = f"{__BASE_API_URL}/personal/message/send"

    """资源API"""
    # 上传资源图片
    SET_RESOURCE_PICTURE_UPLOAD = f"{__BASE_API_URL}/resource/picture/upload"

    """事件API"""
    # 获取WebSocket连接
    GET_WEBSOCKET_CONNECTION = f"{__BASE_API_URL}/websocket/connection"


class MessageType(Enum):
    # 文字消息
    TEXT = 1
    # 图片消息
    IMAGE = 2
    # 视频消息
    VIDEO = 3
    # 分享消息
    SHARE = 4
    # 文件消息
    FILE = 5
    # 卡片消息
    CARD = 6
    # 红包消息
    RED_PACKET = 7


class EventType(Enum):
    # 频道消息
    CHANNEL_MESSAGE = '2001'  # 消息事件
    EMOJI_REACTION = '3001'  # 消息表情反应事件
    CARD_BUTTON_CLICK = '3002'  # 卡片消息按钮事件
    CARD_FORM_SUBMISSION = '3003'  # 卡片消息表单回传事件
    CARD_LIST_SUBMISSION = '3004'  # 卡片消息列表回传事件
    # 语音频道
    MEMBER_JOIN_VOICE_CHANNEL = '5001'  # 成员加入语音频道事件
    MEMBER_EXIT_VOICE_CHANNEL = '5002'  # 成员退出语音频道事件
    # 帖子频道
    POST_PUBLISH = '6001'  # 帖子发布事件
    POST_COMMENT_REPLY = '6002'  # 帖子评论回复事件
    # 成员
    MEMBER_JOIN = '4001'  # 成员加入事件
    MEMBER_EXIT = '4002'  # 成员退出事件
    MEMBER_INVITATION = '4003'  # 成员邀请事件
    # 赠礼系统
    GIFT_SUCCESS = '7001'  # 赠礼成功事件
    # 积分系统
    POINT_CHANGE = '8001'  # 积分变更事件
    # 商城系统
    PURCHASE_SUCCESS = '9001'  # 商品购买成功事件
    # 私信
    PRIVATE_MESSAGE = '1001'  # 私信事件
