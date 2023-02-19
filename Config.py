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
    '0': 'User',
    '1': 'Moderator',
    '2': 'Administrator',
    '3': 'Operator'
}

ALIASES = {
    'ban': ['ban', 'Ban', 'бан', 'Бан', 'блок', 'Блок'],
    'ban_url': ['ban_url', 'Ban_url', 'бан_ссылкой', 'Бан_cсылкой', 'блок_ссылкой', 'Блок_ссылкой'],

    'unban': ['Unban', 'unban', 'Разбан', 'Разбан', 'Разблок', 'разблок'],
    'unban_url': ['Unban_url', 'unban_url', 'Разбан_ссылкой', 'Разбан_ссылкой', 'Разблок_ссылкой', 'разблок_ссылкой'],

    'warn': ['warn', 'Warn', 'варн', 'Варн', 'пред', 'Пред'],
    'warn_url': ['warn_url', 'Warn_url', 'варн_ссылкой', 'Варн_ссылкой', 'пред_ссылкой', 'Пред_ссылкой'],

    'unwarn': ['unwarn', 'Unwarn', 'Разварн', 'разварн', 'Разпред', 'разпред'],
    'unwarn_url': ['unwarn_url', 'Unwarn_url', 'Разварн_ссылкой', 'разварн_ссылкой', 'Распред_ссылкой', 'распред_ссылкой'],

    'delete': ['delete', 'Delete', 'Удалить', 'удалить'],
    'reference': ['reference', 'Reference', 'справка', 'Справка'],
    'set_cooldown': ['set_cooldown', 'Set_cooldown', 'установить_задержку', 'установить_задержку'],
    'set_log_conversation': ['set_log_conversation', 'Set_log_conversation', 'установить_лог_беседу', 'Установить_лог_беседу'],

    'set_permission': ['set_permission', 'Set_permission', 'дать_права', 'Дать_права'],
    'set_permission_url': ['set_permission_url', 'Set_permission_url', 'дать_права_ссылкой', 'Дать_права_ссылкой'],

    'mute': ['mute', 'Mute', 'мут', 'Мут'],
    'mute_url': ['mute_url', 'Mute_url', 'мут_ссылкой', 'Мут_ссылкой'],

    'unmute': ['unmute', 'Unmute', 'размут', 'Размут'],
    'unmute_url': ['unmute_url', 'Unmute_url', 'размут_ссылкой', 'Размут_ссылкой'],

}

