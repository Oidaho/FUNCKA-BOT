"""
Bot main token
"""
TOKEN = 'vk1.a.iOQcZ5g1GtS_Kj7cAYEoy8FuoeTICSg0DXGZ7H5J-f9NP4Kp9LvvzHfbLNBZ_lwhdWr8Io41-LZ9Do9uSoSXlF9EeiQl3Ai0Ob_Oyvxr__KidaYuNLEVQdNL8fabRKJ-TnFdt2f-eHlxJBuVcf1fRQNceWf8lJ1a6IAiWydV2ozRgMyqsWTZIjn31eOJclUHKWWGszuPLBBWZS7i6HU8NA'

"""
Master group id
"""
GROUP = 218730916

"""
Moderation content
"""
BAN_TYPE = {
    'h': 'hour(s)',
    'd': 'day(s)',
    'm': 'month(s)',
    'p': 'permanent'
}

PERMISSION_LVL = {
    '1': 'Moderator',
    '2': 'Administrator'
}

ALIASES = {
    'ban': ['ban', 'Ban', 'бан', 'Бан', 'блок', 'Блок'],
    'unban': ['Unban', 'unban', 'Разбан', 'Разбан', 'Разблок', 'разблок'],
    'warn': ['warn', 'Warn', 'варн', 'Варн', 'пред', 'Пред'],
    'unwarn': ['unwarn', 'Unwarn', 'Разварн', 'разварн', 'Разпред', 'разпред'],
    'delete': ['delete', 'Delete', 'Удалить', 'удалить'],
    'help': ['help', 'Help', 'помощь', 'Помощь'],
    'upperm': ['upperm', 'Upperm', 'поднятьправа', 'Поднятправа'],
    'downperm': ['downperm', 'Downperm', 'Понизитьправа', 'понизитьправа']
}

MESSAGE_COOLDOWN = 30 * 60  # 30 minutes in seconds
