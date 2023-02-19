from vkbottle.bot import Bot, BotLabeler, Message
from typing import Tuple
from Config import GROUP, BAN_TYPE, ALIASES, PERMISSION_LVL, TOKEN
from Rules.CustomRules import HandleCommand, PermissionAccess, HandleRepliedMessages, PermissionIgnore, \
    HandleLogConversation
from urlextract import URLExtract
from DataBase import DataBaseTools as DBtools


bot = Bot(token=TOKEN)
bl = BotLabeler()


@bl.chat_message(
    HandleCommand(ALIASES['ban'], ['!', '/'], 2),
    HandleLogConversation(False),
    PermissionAccess(1),
    PermissionIgnore(1),
    HandleRepliedMessages(True)
)
async def ban(message: Message, args: Tuple[str]):
    if message.fwd_messages:
        for msg in message.fwd_messages:
            ban_users_info = await bot.api.users.get(msg.from_id)
            await call_ban_proc(message, args, ban_users_info)

    else:
        ban_users_info = await bot.api.users.get(message.reply_message.from_id)
        await call_ban_proc(message, args, ban_users_info)


@bl.chat_message(
    HandleCommand(ALIASES['ban_url'], ['!', '/'], 3),
    HandleLogConversation(False),
    PermissionAccess(1),
    PermissionIgnore(1),
    HandleRepliedMessages(False)
)
async def ban_url(message: Message, args: Tuple[str]):
    extractor = URLExtract()
    if extractor.has_urls(args[2]):
        if args[2].startswith('https://vk.com/id'):
            shortname = int(args[2].replace('https://vk.com/id', ''))
            ban_users_info = await bot.api.users.get([shortname])

            await call_ban_proc(message, args, ban_users_info)

        elif args[2].startswith('https://vk.com/'):
            shortname = args[2].replace('https://vk.com/', '')
            ban_users_info = await bot.api.users.get([shortname])

            await call_ban_proc(message, args, ban_users_info)

        else:
            await alert_not_pointing_url(message)

    else:
        await alert_arg_missing_url(message)


@bl.chat_message(
    HandleCommand(ALIASES['warn'], ['!', '/'], 0),
    HandleLogConversation(False),
    PermissionAccess(1),
    PermissionIgnore(1),
    HandleRepliedMessages(True)
)
async def warn(message: Message):
    if message.fwd_messages:
        for msg in message.fwd_messages:
            warn_users_info = await bot.api.users.get(msg.from_id)
            await call_warn_proc(message, warn_users_info)

    else:
        warn_users_info = await bot.api.users.get(message.reply_message.from_id)
        await call_warn_proc(message, warn_users_info)


@bl.chat_message(
    HandleCommand(ALIASES['warn_url'], ['!', '/'], 1),
    HandleLogConversation(False),
    PermissionAccess(1),
    PermissionIgnore(1),
    HandleRepliedMessages(False)
)
async def warn_url(message: Message, args: Tuple[str]):
    extractor = URLExtract()
    if extractor.has_urls(args[0]):
        if args[0].startswith('https://vk.com/id'):
            shortname = int(args[0].replace('https://vk.com/id', ''))
            warn_users_info = await bot.api.users.get([shortname])

            await call_warn_proc(message, warn_users_info)

        elif args[0].startswith('https://vk.com/'):
            shortname = args[0].replace('https://vk.com/', '')
            warn_users_info = await bot.api.users.get([shortname])

            await call_warn_proc(message, warn_users_info)

        else:
            await alert_not_pointing_url(message)

    else:
        await alert_arg_missing_url(message)


@bl.chat_message(
    HandleCommand(ALIASES['delete'], ['!', '/'], 0),
    HandleLogConversation(True),
    PermissionAccess(1),
    HandleRepliedMessages(True)
)
async def delete(message: Message):
    if message.fwd_messages:
        await fwd_msgs_delete(message)
        await self_msg_delete(message)
    # if you called command with one replied messages
    else:
        await rpl_msg_delete(message)
        await self_msg_delete(message)


@bl.chat_message(
    HandleCommand(ALIASES['unban'], ['!', '/'], 0),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(True)
)
async def unban(message: Message):
    unban_users_info = await bot.api.users.get(message.reply_message.from_id)
    await call_unban_proc(message, unban_users_info)


@bl.chat_message(
    HandleCommand(ALIASES['unban_url'], ['!', '/'], 1),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(False)
)
async def unban_url(message: Message, args: Tuple[str]):
    extractor = URLExtract()
    if extractor.has_urls(args[0]):
        if args[0].startswith('https://vk.com/id'):
            shortname = int(args[0].replace('https://vk.com/id', ''))
            unban_users_info = await bot.api.users.get([shortname])

            await call_unban_proc(message, unban_users_info)

        elif args[0].startswith('https://vk.com/'):
            shortname = args[0].replace('https://vk.com/', '')
            unban_users_info = await bot.api.users.get([shortname])

            await call_unban_proc(message, unban_users_info)

        else:
            await alert_not_pointing_url(message)

    else:
        await alert_arg_missing_url(message)


@bl.chat_message(
    HandleCommand(ALIASES['unwarn'], ['!', '/'], 0),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(True)
)
async def unwarn(message: Message):
    unwarn_users_info = await bot.api.users.get(message.reply_message.from_id)
    await call_unwarn_proc(message, unwarn_users_info)


@bl.chat_message(
    HandleCommand(ALIASES['unwarn_url'], ['!', '/'], 1),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(False)
)
async def unwarn_url(message: Message, args: Tuple[str]):
    extractor = URLExtract()

    if extractor.has_urls(args[0]):
        if args[0].startswith('https://vk.com/id'):
            shortname = int(args[0].replace('https://vk.com/id', ''))
            unwarn_users_info = await bot.api.users.get([shortname])

            await call_unwarn_proc(message, unwarn_users_info)

        elif args[0].startswith('https://vk.com/'):
            shortname = args[0].replace('https://vk.com/', '')
            unwarn_users_info = await bot.api.users.get([shortname])

            await call_unwarn_proc(message, unwarn_users_info)

        else:
            await alert_not_pointing_url(message)

    else:
        await alert_arg_missing_url(message)


@bl.chat_message(
    HandleCommand(ALIASES['reference'], ['!', '/'], 0),
    HandleLogConversation(True),
    PermissionAccess(1),
    HandleRepliedMessages(False)
)
async def reference(message: Message):
    users_info = await bot.api.users.get(message.from_id)

    title = f'@id{users_info[0].id} ({users_info[0].first_name}), вот реализованый список команд: \n' \
            f'· warn - Выдать предупреждение пользователю (in work)\n' \
            f'· unwarn - Снять предупреждение с пользователя (in work)\n' \
            f'· ban \'time\' \'time_type\' - Заблокировать пользователя (in work)\n' \
            f'· unban - Разблокировать пользователя (in work)\n' \
            f'· delete - Удалить сообщение (done)\n' \
            f'· upperm \'n\' - Повысить уровень прав на \'n\' пунктов (in work)\n' \
            f'· downperm \'n\' - Понизить уровень прав на \'n\' пунктов (in work)\n'
    await message.answer(title)

    title = f'Список реализованых систем:\n' \
            f'· URL Filter (in work)\n' \
            f'· Forbidden Filter (in work)\n' \
            f'· Group Answerer (done)'
    await message.answer(title)

    await self_msg_delete(message)


@bl.chat_message(
    HandleCommand(ALIASES['set_permission'], ['!', '/'], 1),
    HandleLogConversation(True),
    PermissionAccess(2),
    HandleRepliedMessages(True)
)
async def set_permission(message: Message, args: Tuple[str]):
    try:
        permission_lvl = int(args[0])  # Catching exception here
        if permission_lvl > 3 or permission_lvl < 0:
            permission_lvl = 0

        users_info = await bot.api.users.get(message.reply_message.from_id)

        if users_info:
            if DBtools.set_permission(message, users_info[0].id, permission_lvl):
                await alert_permission_changed(message, users_info, permission_lvl)

            else:
                await alert_permission_not_changed(message)

        else:
            title = f'Пользователю не может быть установленна группа прав или пользователь не найден.'
            await message.answer(title)
            await self_msg_delete(message)

    except TypeError:
        await alert_wrong_arg(message)


@bl.chat_message(
    HandleCommand(ALIASES['set_permission_url'], ['!', '/'], 2),
    HandleLogConversation(True),
    PermissionAccess(2),
    HandleRepliedMessages(False)
)
async def set_permission_url(message: Message, args: Tuple[str]):
    try:
        permission_lvl = int(args[0])
        if permission_lvl > 3:
            permission_lvl = 0

        extractor = URLExtract()

        if extractor.has_urls(args[1]):
            if args[1].startswith('https://vk.com/id'):
                shortname = int(args[1].replace('https://vk.com/id', ''))
                users_info = await bot.api.users.get([shortname])

                if DBtools.set_permission(message, users_info[0].id, permission_lvl):
                    await alert_permission_changed(message, users_info, permission_lvl)

                else:
                    await alert_permission_not_changed(message)

            elif args[1].startswith('https://vk.com/'):
                shortname = args[1].replace('https://vk.com/', '')
                users_info = await bot.api.users.get([shortname])

                if DBtools.set_permission(message, users_info[0].id, permission_lvl):
                    await alert_permission_changed(message, users_info, permission_lvl)

                else:
                    await alert_permission_not_changed(message)

            else:
                await alert_not_pointing_url(message)

        else:
            await alert_arg_missing_url(message)

    except TypeError:
        await alert_wrong_arg(message)


@bl.chat_message(
    HandleCommand(ALIASES['set_cooldown'], ['!', '/'], 1),
    HandleLogConversation(False),
    PermissionAccess(2),
    HandleRepliedMessages(False)
)
async def set_cooldown(message: Message, args: Tuple[str]):
    try:
        cooldown = int(args[0])  # Catching exception here
        if DBtools.set_cooldown(message, cooldown):
            users_info = await bot.api.users.get(message.from_id)
            title = f'@id{users_info[0].id} ({users_info[0].first_name}), ' \
                    f'задержка на сообщения для данной беседы установлена на {cooldown} second(s).'
            await message.answer(title)
            await self_msg_delete(message)

    except TypeError:
        await alert_wrong_arg(message)


@bl.chat_message(
    HandleCommand(ALIASES['set_log_conversation'], ['!', '/'], 0),
    HandleLogConversation(True),
    PermissionAccess(2),
    HandleRepliedMessages(False)
)
async def set_log_conversation(message: Message):
    if DBtools.set_log_conversation(message):
        title = f'Данная беседа теперь назначена в качестве лог-чата.'
        await message.answer(title)

    else:
        title = f'Данная беседа уже назначена в качестве лог-чата.'
        await message.answer(title)

    await self_msg_delete(message)

'''
-----------------------------------------------------------------------------------------------------------------------
'''


async def call_ban_proc(message: Message, args: Tuple[str], bui):
    ban_users_info = bui

    if not ban_users_info:
        await alert_user_not_found(message)

    else:
        time = args[0]
        time_type = BAN_TYPE[args[1]]

        if args[1] == 'p':
            time = ''
        elif args[1] == 'm':
            if int(time) < 0:
                time = '1'
            if int(time) > 12:
                time = '12'
        elif args[1] == 'd':
            if int(time) < 0:
                time = '1'
            if int(time) > 31:
                time = '31'
        elif args[1] == 'h':
            if int(time) < 0:
                time = '1'
            if int(time) > 24:
                time = '24'
        else:
            time = '1'
            time_type = BAN_TYPE['d']

        title = f'@id{ban_users_info[0].id} (Пользователь) ' \
                f'был заблокирован на {time} {time_type}.'

        if time == '' and time_type == 'permanent':
            if DBtools.add_permanent_ban(message):
                await message.answer(title)
                await self_msg_delete(message)
                await rpl_msg_delete(message)
                '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''

            else:
                await alert_already_banned(message)

        else:
            if DBtools.add_temp_ban(message, ban_users_info[0].id, time, time_type):
                await message.answer(title)
                await self_msg_delete(message)
                await rpl_msg_delete(message)
                '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''

            else:
                await alert_already_banned(message)


async def call_warn_proc(message: Message, wui):
    warn_users_info = wui

    if not warn_users_info:
        title = f'Пользователь ' \
                f'не может быть предупреждён или не существует.'
        await message.answer(title)
        await self_msg_delete(message)

    else:
        warn_count = DBtools.get_warn_count(message, warn_users_info[0].id)

        title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                f'получил предупреждение [{warn_count + 1}/3].'
        await message.answer(title)

        DBtools.add_warn(message, warn_users_info[0].id, warn_count + 1)

        if warn_count + 1 == 3:
            time = '3'
            time_type = BAN_TYPE['d']

            title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                    f'был заблокирован на {time} {time_type}.'

            if DBtools.add_temp_ban(message, warn_users_info[0].id, time, time_type):
                await message.answer(title)
                await self_msg_delete(message)
                await rpl_msg_delete(message)
                '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''

            else:
                await alert_already_banned(message)

        await self_msg_delete(message)
        await rpl_msg_delete(message)


async def call_unban_proc(message: Message, uui):
    unban_users_info = uui
    if unban_users_info:
        user_id = unban_users_info[0].id

        ban_kind = DBtools.get_ban_kind(message, user_id)
        if ban_kind == 'permanent':
            if DBtools.remove_permanent_ban(message, user_id):
                await alert_unbanned(message, unban_users_info)

            else:
                await alert_user_not_found_DB(message)

        elif ban_kind == 'temp':
            if DBtools.remove_temp_ban(message, user_id):
                await alert_unbanned(message, unban_users_info)

            else:
                await alert_user_not_found_DB(message)

        else:
            await alert_user_not_found_DB(message)

    else:
        await alert_user_not_found(message)


async def call_unwarn_proc(message: Message, uui):
    unwarn_users_info = uui
    if unwarn_users_info:
        user_id = unwarn_users_info[0].id

        warn_count = DBtools.get_warn_count(message, user_id)

        if warn_count != 0:

            DBtools.remove_warn(message, user_id, warn_count)

            title = f'С @id{unwarn_users_info[0].id} (пользователя) снято предупреждение.\n' \
                    f'Текущее кол-во предупреждений [{warn_count - 1}/3]'
            await message.answer(title)
            await self_msg_delete(message)

        else:
            await alert_user_not_found_DB(message)

    else:
        await alert_user_not_found(message)


'''
-----------------------------------------------------------------------------------------------------------------------
'''


async def alert_wrong_arg(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    title = f'@id{users_info[0].id} ({users_info[0].first_name}), аргумент указан неверно.'
    await message.answer(title)
    await self_msg_delete(message)


async def alert_permission_changed(message: Message, users_info, permission_lvl):
    title = f'Группа прав @id{users_info[0].id} (пользователя), ' \
            f'была изменена на {permission_lvl} ({PERMISSION_LVL[str(permission_lvl)]}).'
    await message.answer(title)
    await self_msg_delete(message)


async def alert_permission_not_changed(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    title = f'@id{users_info[0].id} ({users_info[0].first_name}), ' \
            f'группа прав пользователя не была изменена.'
    await message.answer(title)
    await self_msg_delete(message)


async def alert_command_access_denied(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    title = f'@id{users_info[0].id} ({users_info[0].first_name}), вам не доступна данная команда.'
    await message.answer(title)
    await self_msg_delete(message)


async def alert_already_banned(message: Message):
    ban_users_info = await bot.api.users.get(message.reply_message.from_id)
    title = f'@id{ban_users_info[0].id} (Пользователь) уже заблокирован.'
    await message.answer(title)
    await self_msg_delete(message)


async def alert_unbanned(message: Message, uui):
    title = f'С @id{uui[0].id} (пользователя) снята блокировка.\n' \
            f'Теперь он снова может зайти в беседу.'
    await message.answer(title)
    await self_msg_delete(message)


async def alert_user_not_found_DB(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    title = f'@id{users_info[0].id} ({users_info[0].first_name}), пользователь не найден в базе данных.'
    await message.answer(title)
    await self_msg_delete(message)


async def alert_user_not_found(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    title = f'@id{users_info[0].id} ({users_info[0].first_name}), ' \
            f'к пользователю не может быть применена команда или пользователь не существует.'
    await message.answer(title)
    await self_msg_delete(message)


async def alert_not_pointing_url(message: Message):
    users_info = await bot.api.users.get(message.from_id)

    title = f'@id{users_info[0].id} ({users_info[0].first_name}), ссылка не указывает на профиль ' \
            f'пользователя.'
    await message.answer(title)
    await self_msg_delete(message)


async def alert_arg_missing_url(message: Message):
    users_info = await bot.api.users.get(message.from_id)

    title = f'@id{users_info[0].id} ({users_info[0].first_name}), в аргументе команды отсутствует сылка.'
    await message.answer(title)
    await self_msg_delete(message)


async def alert_using_both_methods(message: Message):
    users_info = await bot.api.users.get(message.from_id)

    title = f'@id{users_info[0].id} ({users_info[0].first_name}), ' \
            f'нельзя использовать аргументный и пересыльный метод одновременно.\n' \
            f'Попробуйте использовать что-то одно.'
    await message.answer(title)
    await self_msg_delete(message)


async def alert_forbidden_to_group(message: Message):
    users_info = await bot.api.users.get(message.from_id)

    title = f'@id{users_info[0].id} ({users_info[0].first_name}), ' \
            f'нельзя применить команду к группе сообщений.'
    await message.answer(title)
    await self_msg_delete(message)


async def alert_forbidden_to_self(message: Message):
    users_info = await bot.api.users.get(message.from_id)

    title = f'@id{users_info[0].id} ({users_info[0].first_name}), ' \
            f'нельзя применить команду к своему сообщению.'
    await message.answer(title)
    await self_msg_delete(message)

'''
-----------------------------------------------------------------------------------------------------------------------
'''


async def self_msg_delete(message: Message):
    message_id = message.conversation_message_id
    peer_id = message.peer_id
    await bot.api.messages.delete(group_id=GROUP, peer_id=peer_id, cmids=message_id, delete_for_all=True)


async def rpl_msg_delete(message: Message):
    if message.reply_message is not None:
        message_id = message.reply_message.conversation_message_id
        peer_id = message.peer_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=peer_id, cmids=message_id, delete_for_all=True)


async def fwd_msgs_delete(message: Message):
    if message.fwd_messages:
        for msg in message.fwd_messages:
            message_id = msg.conversation_message_id
            peer_id = message.peer_id
            await bot.api.messages.delete(group_id=GROUP, peer_id=peer_id, cmids=message_id, delete_for_all=True)
