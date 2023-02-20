from vkbottle.bot import Bot, BotLabeler, Message
from typing import Tuple
from Config import BAN_TYPE, ALIASES, TOKEN, SETTINGS
from Log import Logger as ol
from Alert import Alerter as oa
from Rules.CustomRules import (
    HandleCommand,
    PermissionAccess,
    HandleRepliedMessages,
    PermissionIgnore,
    HandleLogConversation
)
from urlextract import URLExtract
from DataBase import DataBaseTools as DBtools

bot = Bot(token=TOKEN)
bl = BotLabeler()


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


@bl.chat_message(
    HandleCommand(ALIASES['ban'], ['!', '/'], 2),
    HandleLogConversation(False),
    PermissionAccess(1),
    PermissionIgnore(1),
    HandleRepliedMessages(True)
)
async def ban(message: Message, args: Tuple[str]):
    if message.fwd_messages:
        ids = set(msg.from_id for msg in message.fwd_messages)
        for user_id in ids:
            ban_users_info = await bot.api.users.get(user_id)
            if not ban_users_info:
                title = f'Пользователь ' \
                        f'не может быть заблокирован.'
                await message.answer(title)

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
                    if DBtools.add_permanent_ban(message, ban_users_info[0].id):
                        await message.answer(title)
                        await ol.log_banned(message, ban_users_info, time, time_type)
                        await oa.rpl_msg_delete(message)

                        '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''

                else:
                    if DBtools.add_temp_ban(message, ban_users_info[0].id, time, time_type):
                        await message.answer(title)
                        await ol.log_banned(message, ban_users_info, time, time_type)
                        await oa.rpl_msg_delete(message)

                        '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''

    else:
        ban_users_info = await bot.api.users.get(message.reply_message.from_id)
        if not ban_users_info:
            title = f'Пользователь ' \
                    f'не может быть заблокирован.'
            await message.answer(title)

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
                if DBtools.add_permanent_ban(message, ban_users_info[0].id):
                    await message.answer(title)
                    await ol.log_banned(message, ban_users_info, time, time_type)
                    await oa.rpl_msg_delete(message)

                    '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''

            else:
                if DBtools.add_temp_ban(message, ban_users_info[0].id, time, time_type):
                    await message.answer(title)
                    await ol.log_banned(message, ban_users_info, time, time_type)
                    await oa.rpl_msg_delete(message)

                    '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''


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

            if not ban_users_info:
                title = f'Пользователь ' \
                        f'не может быть заблокирован.'
                await message.answer(title)

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
                    if DBtools.add_permanent_ban(message, ban_users_info[0].id):
                        await message.answer(title)
                        await ol.log_banned_url(message, ban_users_info, time, time_type)
                        await oa.rpl_msg_delete(message)

                        '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''

                else:
                    if DBtools.add_temp_ban(message, ban_users_info[0].id, time, time_type):
                        await message.answer(title)
                        await ol.log_banned_url(message, ban_users_info, time, time_type)
                        await oa.rpl_msg_delete(message)

                        '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''

        elif args[2].startswith('https://vk.com/'):
            shortname = args[2].replace('https://vk.com/', '')
            ban_users_info = await bot.api.users.get([shortname])

            if not ban_users_info:
                title = f'Пользователь ' \
                        f'не может быть заблокирован.'
                await message.answer(title)

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
                    if DBtools.add_permanent_ban(message, ban_users_info[0].id):
                        await message.answer(title)
                        await ol.log_banned_url(message, ban_users_info, time, time_type)
                        await oa.rpl_msg_delete(message)

                        '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''

                else:
                    if DBtools.add_temp_ban(message, ban_users_info[0].id, time, time_type):
                        await message.answer(title)
                        await ol.log_banned_url(message, ban_users_info, time, time_type)
                        await oa.rpl_msg_delete(message)

                        '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''


@bl.chat_message(
    HandleCommand(ALIASES['warn'], ['!', '/'], 0),
    HandleLogConversation(False),
    PermissionAccess(1),
    PermissionIgnore(1),
    HandleRepliedMessages(True)
)
async def warn(message: Message):
    if message.fwd_messages:
        ids = set(msg.from_id for msg in message.fwd_messages)
        for user_id in ids:
            warn_users_info = await bot.api.users.get(user_id)

            if not warn_users_info:
                title = f'Пользователь ' \
                        f'не может быть предупреждён.'
                await message.answer(title)

            else:
                warn_count = DBtools.get_warn_count(message, warn_users_info[0].id)

                title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                        f'получил предупреждение [{warn_count + 1}/3].'
                await message.answer(title)

                if DBtools.add_warn(message, warn_users_info[0].id, warn_count + 1):
                    await ol.log_warned(message, warn_users_info, warn_count + 1)

                if warn_count + 1 == 3:
                    time = '3'
                    time_type = BAN_TYPE['d']

                    title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                            f'был заблокирован на {time} {time_type}.'

                    if DBtools.add_temp_ban(message, warn_users_info[0].id, time, time_type):
                        await message.answer(title)
                        await ol.log_system_banned(message, warn_users_info, time, time_type)
                        await oa.rpl_msg_delete(message)
                        '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''

    else:
        warn_users_info = await bot.api.users.get(message.reply_message.from_id)
        if not warn_users_info:
            title = f'Пользователь ' \
                    f'не может быть предупреждён.'
            await message.answer(title)

        else:
            warn_count = DBtools.get_warn_count(message, warn_users_info[0].id)

            title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                    f'получил предупреждение [{warn_count + 1}/3].'
            await message.answer(title)

            if DBtools.add_warn(message, warn_users_info[0].id, warn_count + 1):
                await ol.log_warned(message, warn_users_info, warn_count + 1)

            if warn_count + 1 == 3:
                time = '3'
                time_type = BAN_TYPE['d']

                title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                        f'был заблокирован на {time} {time_type}.'

                if DBtools.add_temp_ban(message, warn_users_info[0].id, time, time_type):
                    await message.answer(title)
                    await ol.log_system_banned(message, warn_users_info, time, time_type)
                    await oa.rpl_msg_delete(message)
                    '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''


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

            if not warn_users_info:
                title = f'Пользователь ' \
                        f'не может быть предупреждён или не существует.'
                await message.answer(title)

            else:
                warn_count = DBtools.get_warn_count(message, warn_users_info[0].id)

                title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                        f'получил предупреждение [{warn_count + 1}/3].'
                await message.answer(title)

                if DBtools.add_warn(message, warn_users_info[0].id, warn_count + 1):
                    await ol.log_warned_url(message, warn_users_info, warn_count + 1)

                if warn_count + 1 == 3:
                    time = '3'
                    time_type = BAN_TYPE['d']

                    title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                            f'был заблокирован на {time} {time_type}.'

                    if DBtools.add_temp_ban(message, warn_users_info[0].id, time, time_type):
                        await message.answer(title)
                        await ol.log_system_banned(message, warn_users_info, time, time_type)
                        await oa.rpl_msg_delete(message)
                        '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''

        elif args[0].startswith('https://vk.com/'):
            shortname = args[0].replace('https://vk.com/', '')
            warn_users_info = await bot.api.users.get([shortname])

            if not warn_users_info:
                title = f'Пользователь ' \
                        f'не может быть предупреждён или не существует.'
                await message.answer(title)

            else:
                warn_count = DBtools.get_warn_count(message, warn_users_info[0].id)

                title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                        f'получил предупреждение [{warn_count + 1}/3].'
                await message.answer(title)

                if DBtools.add_warn(message, warn_users_info[0].id, warn_count + 1):
                    await ol.log_warned_url(message, warn_users_info, warn_count + 1)

                if warn_count + 1 == 3:
                    time = '3'
                    time_type = BAN_TYPE['d']

                    title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                            f'был заблокирован на {time} {time_type}.'

                    if DBtools.add_temp_ban(message, warn_users_info[0].id, time, time_type):
                        await message.answer(title)
                        await ol.log_system_banned(message, warn_users_info, time, time_type)
                        await oa.rpl_msg_delete(message)
                        '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''


@bl.chat_message(
    HandleCommand(ALIASES['unban'], ['!', '/'], 0),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(True)
)
async def unban(message: Message):
    unban_users_info = await bot.api.users.get(message.reply_message.from_id)
    if unban_users_info:
        user_id = unban_users_info[0].id

        ban_kind = DBtools.get_ban_kind(message, user_id)
        if ban_kind == 'permanent':
            if DBtools.remove_permanent_ban(message, user_id):
                await ol.log_unbanned(message, unban_users_info)
                await oa.alert_unbanned(message, unban_users_info)

        elif ban_kind == 'temp':
            if DBtools.remove_temp_ban(message, user_id):
                await ol.log_unbanned(message, unban_users_info)
                await oa.alert_unbanned(message, unban_users_info)


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
            if unban_users_info:
                user_id = unban_users_info[0].id

                ban_kind = DBtools.get_ban_kind(message, user_id)
                if ban_kind == 'permanent':
                    if DBtools.remove_permanent_ban(message, user_id):
                        await ol.log_unbanned_url(message, unban_users_info)
                        await oa.alert_unbanned(message, unban_users_info)

                elif ban_kind == 'temp':
                    if DBtools.remove_temp_ban(message, user_id):
                        await ol.log_unbanned_url(message, unban_users_info)
                        await oa.alert_unbanned(message, unban_users_info)

        elif args[0].startswith('https://vk.com/'):
            shortname = args[0].replace('https://vk.com/', '')
            unban_users_info = await bot.api.users.get([shortname])

            if unban_users_info:
                user_id = unban_users_info[0].id

                ban_kind = DBtools.get_ban_kind(message, user_id)
                if ban_kind == 'permanent':
                    if DBtools.remove_permanent_ban(message, user_id):
                        await ol.log_unbanned_url(message, unban_users_info)
                        await oa.alert_unbanned(message, unban_users_info)

                elif ban_kind == 'temp':
                    if DBtools.remove_temp_ban(message, user_id):
                        await ol.log_unbanned_url(message, unban_users_info)
                        await oa.alert_unbanned(message, unban_users_info)


# TODO: Добавить множественный анварн
@bl.chat_message(
    HandleCommand(ALIASES['unwarn'], ['!', '/'], 0),
    HandleLogConversation(False),
    PermissionAccess(1),
    HandleRepliedMessages(True)
)
async def unwarn(message: Message):
    unwarn_users_info = await bot.api.users.get(message.reply_message.from_id)
    if unwarn_users_info:
        user_id = unwarn_users_info[0].id

        warn_count = DBtools.get_warn_count(message, user_id)

        if warn_count != 0:
            DBtools.remove_warn(message, user_id, warn_count)

            title = f'С @id{unwarn_users_info[0].id} (пользователя) снято предупреждение.\n' \
                    f'Текущее кол-во предупреждений [{warn_count - 1}/3]'
            await message.answer(title)
            await ol.log_unwarned(message, unwarn_users_info, warn_count - 1)


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

            if unwarn_users_info:
                user_id = unwarn_users_info[0].id

                warn_count = DBtools.get_warn_count(message, user_id)

                if warn_count != 0:
                    DBtools.remove_warn(message, user_id, warn_count)

                    title = f'С @id{unwarn_users_info[0].id} (пользователя) снято предупреждение.\n' \
                            f'Текущее кол-во предупреждений [{warn_count - 1}/3]'
                    await message.answer(title)
                    await ol.log_unwarned_url(message, unwarn_users_info, warn_count)

        elif args[0].startswith('https://vk.com/'):
            shortname = args[0].replace('https://vk.com/', '')
            unwarn_users_info = await bot.api.users.get([shortname])

            if unwarn_users_info:
                user_id = unwarn_users_info[0].id

                warn_count = DBtools.get_warn_count(message, user_id)

                if warn_count != 0:
                    DBtools.remove_warn(message, user_id, warn_count)

                    title = f'С @id{unwarn_users_info[0].id} (пользователя) снято предупреждение.\n' \
                            f'Текущее кол-во предупреждений [{warn_count - 1}/3]'
                    await message.answer(title)
                    await ol.log_unwarned_url(message, unwarn_users_info, warn_count)


@bl.chat_message(
    HandleCommand(ALIASES['delete'], ['!', '/'], 0),
    HandleLogConversation(True),
    PermissionAccess(1),
    HandleRepliedMessages(True)
)
async def delete(message: Message):
    if message.fwd_messages:
        await ol.log_deleted(message)
        await oa.fwd_msgs_delete(message)

    else:
        await ol.log_deleted(message)
        await oa.rpl_msg_delete(message)


@bl.chat_message(
    HandleCommand(ALIASES['set_permission'], ['!', '/'], 1),
    HandleLogConversation(True),
    PermissionAccess(2),
    HandleRepliedMessages(True)
)
async def set_permission(message: Message, args: Tuple[str]):
    if not message.fwd_messages:
        try:
            permission_lvl = int(args[0])  # Catching exception here
            if permission_lvl > 3 or permission_lvl < 0:
                permission_lvl = 0

            users_info = await bot.api.users.get(message.reply_message.from_id)

            if users_info:
                if DBtools.set_permission(message, users_info[0].id, permission_lvl):
                    await ol.log_permission_changed(message, users_info, permission_lvl)
                    await oa.alert_permission_changed(message, users_info, permission_lvl)

            else:
                title = f'Пользователю не может быть установленна группа прав.'
                await message.answer(title)

        except TypeError:
            pass


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
                    await oa.alert_permission_changed(message, users_info, permission_lvl)
                    await ol.log_permission_changed(message, users_info, permission_lvl)

            elif args[1].startswith('https://vk.com/'):
                shortname = args[1].replace('https://vk.com/', '')
                users_info = await bot.api.users.get([shortname])

                if DBtools.set_permission(message, users_info[0].id, permission_lvl):
                    await ol.log_permission_changed_url(message, users_info, permission_lvl)
                    await oa.alert_permission_changed(message, users_info, permission_lvl)

    except TypeError:
        pass


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
            await ol.log_cooldown_changed(message, cooldown)

    except TypeError:
        pass


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
        await ol.log_log_conversation_changed(message)

    else:
        title = f'Данная беседа уже назначена в качестве лог-чата.'
        await message.answer(title)


@bl.chat_message(
    HandleCommand(ALIASES['change_setting'], ['!', '/'], 2),
    HandleLogConversation(False),
    PermissionAccess(2),
    HandleRepliedMessages(False)
)
async def change_setting(message: Message, args: Tuple[str]):
    try:
        setting = str(args[0])
        value = str(args[1]).lower()

        if value == 'true':
            value = True

        elif value == 'false':
            value = False

        if setting in SETTINGS and isinstance(value, bool):
            if DBtools.change_setting(message, setting, value):
                title = f'Настройка {setting} изменена на значение {value}.'
                await message.answer(title)
                await ol.log_setting_changed(message, setting, value)

    except TypeError:
        pass
