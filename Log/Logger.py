import datetime
import json

from vkbottle.bot import Bot, Message
from Config import GROUP, PERMISSION_LVL, TOKEN
from DataBase import DataBaseTools as DBtools

bot = Bot(token=TOKEN)


async def log_banned(message: Message, users_info, time, time_type):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) заблокировал ' \
            f'данного @id{users_info[0].id} (пользователя) ' \
            f'на {time} {time_type}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    forward = {
        'peer_id': message.peer_id,
        'conversation_message_ids': [message.reply_message.conversation_message_id],
    }
    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_banned_url(message: Message, users_info, time, time_type):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) заблокировал ' \
            f'данного @id{users_info[0].id} (пользователя) ' \
            f'на {time} {time_type}, используя ссылку\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_system_banned(message: Message, users_info, time, time_type):
    LOG_PEER = DBtools.get_log_conversation()

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'Система заблокировала ' \
            f'данного @id{users_info[0].id} (пользователя) ' \
            f'на {time} {time_type}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_warned(message: Message, users_info, warn_count):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) выдал ' \
            f'предупреждение @id{users_info[0].id} (пользователю)\n' \
            f'Количество предупреждений: {warn_count}/3\n' \
            f'Предупреждения будут сняты через сутки\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    forward = {
        'peer_id': message.peer_id,
        'conversation_message_ids': [message.reply_message.conversation_message_id],
    }
    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_warned_url(message: Message, users_info, warn_count):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) выдал ' \
            f'предупреждение @id{users_info[0].id} (пользователю), используя ссылку\n' \
            f'Количество предупреждений: {warn_count}/3\n' \
            f'Предупреждения будут сняты через сутки\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_unbanned(message: Message, users_info):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) разблокировал ' \
            f'данного @id{users_info[0].id} (пользователя)\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    forward = {
        'peer_id': message.peer_id,
        'conversation_message_ids': [message.reply_message.conversation_message_id],
    }
    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_unbanned_url(message: Message, users_info):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) разблокировал ' \
            f'данного @id{users_info[0].id} (пользователя), используя ссылку\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_unwarned(message: Message, users_info, warn_count):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) снял ' \
            f'предупреждение с @id{users_info[0].id} (пользователя)\n' \
            f'Количество предупреждений: {warn_count}/3\n' \
            f'Предупреждения будут сняты через сутки\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    forward = {
        'peer_id': message.peer_id,
        'conversation_message_ids': [message.reply_message.conversation_message_id],
    }
    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_unwarned_url(message: Message, users_info, warn_count):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) снял ' \
            f'предупреждение с @id{users_info[0].id} (пользователя), используя ссылку\n' \
            f'Количество предупреждений: {warn_count}/3\n' \
            f'Предупреждения будут сняты через сутки\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_deleted(message: Message):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) удалил сообщения\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    if message.fwd_messages:
        forward = {
            'peer_id': message.peer_id,
            'conversation_message_ids': [msg.conversation_message_id for msg in message.fwd_messages],
        }

    else:
        forward = {
            'peer_id': message.peer_id,
            'conversation_message_ids': [message.reply_message.conversation_message_id],
        }

    forward = json.dumps(forward)
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        forward=forward,
        random_id=0
    )


async def log_log_conversation_changed(message: Message):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) ' \
            f'установил новую беседу в качестве лог-чата\n' \
            f'ID источника: {message.peer_id}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_cooldown_changed(message: Message, cooldown):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) ' \
            f'установил новую задержку.\n' \
            f'Задержка: {cooldown} second(s)\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'
    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_permission_changed(message: Message, users_info, permission_lvl):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) изменил группу прав для ' \
            f'данного @id{users_info[0].id} (пользователя) ' \
            f'на {permission_lvl} уровень ({PERMISSION_LVL[str(permission_lvl)]})\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_permission_changed_url(message: Message, users_info, permission_lvl):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) изменил группу прав для ' \
            f'данного @id{users_info[0].id} (пользователя) ' \
            f'на {permission_lvl} уровень ({PERMISSION_LVL[str(permission_lvl)]}), ' \
            f'используя ссылку\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )


async def log_setting_changed(message: Message, setting, value):
    LOG_PEER = DBtools.get_log_conversation()

    author_permission = DBtools.get_permission(message, message.from_id)
    author_id = message.from_id
    if author_permission == 1:
        author_permission = 'Модератор'

    elif author_permission == 2:
        author_permission = 'Администратор'

    conversations_info = await bot.api.messages.get_conversations_by_id(group_id=GROUP, peer_ids=message.peer_id)
    conversations_name = conversations_info.items[0].chat_settings.title

    offset = datetime.timezone(datetime.timedelta(hours=3))
    Moscow_time = str(datetime.datetime.now(offset)).split('.')[0]

    title = f'@id{author_id} ({author_permission}) изменил настройку ' \
            f'{setting} на значение {value}\n' \
            f'Источник: {conversations_name}\n' \
            f'Время (МСК): {Moscow_time}'

    await bot.api.messages.send(
        group_id=GROUP,
        peer_id=LOG_PEER,
        message=title,
        random_id=0
    )
