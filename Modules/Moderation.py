from vkbottle.bot import Bot, BotLabeler, Message
from typing import Tuple

from Config import TOKEN, GROUP, BAN_TYPE, ALIASES
from CustomRules import CommandRuleCustom

bot = Bot(token=TOKEN)
bl = BotLabeler()


@bl.chat_message(CommandRuleCustom(ALIASES['ban'], ['!', '/'], 2))
async def ban(message: Message, args: Tuple[str]):
    # if you want to ban something user
    if (message.reply_message is not None) and (message.reply_message.from_id != message.from_id):
        users_info = await bot.api.users.get(message.from_id)
        ban_users_info = await bot.api.users.get(message.reply_message.from_id)

        if not ban_users_info:
            title = f'@id{users_info[0].id} (Пользователь) ' \
                    f'не может быть предупреждён или не существует.'
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
            await message.answer(title)

            # TODO: Ban procedure somewhere

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

        message_id = message.reply_message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

        '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''

    # if you want to ban yourself
    elif (message.reply_message is not None) and (message.reply_message.from_id == message.from_id):
        users_info = await bot.api.users.get(message.from_id)

        title = f'@id{users_info[0].id} ({users_info[0].first_name}), ' \
                f'нельзя применить команду к своему сообщению.'
        await message.answer(title)

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you called command with more than one replied message
    elif message.fwd_messages and message.reply_message is None:
        users_info = await bot.api.users.get(message.from_id)

        title = f'@id{users_info[0].id} ({users_info[0].first_name}), ' \
                f'нельзя применить команду к группе сообщений.'
        await message.answer(title)

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you called command w\o replied message
    elif message.reply_message is None:
        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)


@bl.chat_message(CommandRuleCustom(ALIASES['warn'], ['!', '/'], 0))
async def warn(message: Message):
    # if you want to warn something user
    if (message.reply_message is not None) and (message.reply_message.from_id != message.from_id):
        users_info = await bot.api.users.get(message.from_id)
        warn_users_info = await bot.api.users.get(message.reply_message.from_id)

        # TODO: Make DB request to get current user's warn count

        warn_count = 0
        if not warn_users_info:
            title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                    f'не может быть предупреждён или не существует.'
            await message.answer(title)

        else:
            title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                    f'получил предупреждение [{warn_count+1}/3].'
            await message.answer(title)

            # TODO: Warn procedure somewhere

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

        message_id = message.reply_message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you want to warn yourself
    elif (message.reply_message is not None) and (message.reply_message.from_id == message.from_id):
        users_info = await bot.api.users.get(message.from_id)

        title = f'@id{users_info[0].id} ({users_info[0].first_name}), ' \
                f'нельзя применить команду к своему сообщению.'
        await message.answer(title)

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you called command with more than one replied message
    elif message.fwd_messages and message.reply_message is None:
        users_info = await bot.api.users.get(message.from_id)

        title = f'@id{users_info[0].id} ({users_info[0].first_name}), ' \
                f'нельзя применить команду к группе сообщений.'
        await message.answer(title)

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you called command w\o replied message
    elif message.reply_message is None:
        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)


@bl.chat_message(CommandRuleCustom(ALIASES['delete'], ['!', '/'], 0))
async def delete(message: Message):
    # if you called command with one replied messages
    if message.reply_message is not None:
        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

        message_id = message.reply_message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you called command with more than one replied messages
    elif message.reply_message is None and message.fwd_messages is not None:
        for msg in message.fwd_messages:
            message_id = msg.conversation_message_id
            await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you called command w\o replied message
    elif message.reply_message is None:
        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)


@bl.chat_message(CommandRuleCustom(ALIASES['unban'], ['!', '/'], 0))
async def unban(message: Message):
    pass


@bl.chat_message(CommandRuleCustom(ALIASES['unwarn'], ['!', '/'], 1))
async def unwarn(message: Message):
    pass


@bl.chat_message(CommandRuleCustom(ALIASES['help'], ['!', '/'], 0))
async def help(message: Message):
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

    message_id = message.conversation_message_id
    await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)


@bl.chat_message(CommandRuleCustom(ALIASES['upperm'], ['!', '/'], 1))
async def upperm(message: Message, args: Tuple[str]):
    pass


@bl.chat_message(CommandRuleCustom(ALIASES['downperm'], ['!', '/'], 1))
async def downperm(message: Message, args: Tuple[str]):
    pass
