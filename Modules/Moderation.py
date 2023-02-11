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

        # TODO: Reply_message can be None, need to catch it. It's happening when yoy trying reply more than one message
        message_id = message.reply_message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you want to ban yourself
    elif message.reply_message.from_id == message.from_id:
        users_info = await bot.api.users.get(message.from_id)

        title = f'@id{users_info[0].id} ({users_info[0].first_name}), ' \
                f'нельзя применить команду к своему сообщению.'
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

        if not warn_users_info:
            title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                    f'не может быть предупреждён или не существует.'
            await message.answer(title)

        else:
            title = f'@id{warn_users_info[0].id} (Пользователь) ' \
                    f'получил предупреждение [0/3].'
            await message.answer(title)

            # TODO: Warn procedure somewhere

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

        # TODO: Reply_message can be None, need to catch it. It's happening when yoy trying reply more than one message
        message_id = message.reply_message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you want to warn yourself
    elif message.reply_message.from_id == message.from_id:
        users_info = await bot.api.users.get(message.from_id)

        title = f'@id{users_info[0].id} ({users_info[0].first_name}), ' \
                f'нельзя применить команду к своему сообщению.'
        await message.answer(title)

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you called command w\o replied message
    elif message.reply_message is None:
        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)


@bl.chat_message(CommandRuleCustom(ALIASES['delete'], ['!', '/'], 0))
async def delete(message: Message):
    if message.reply_message is not None:
        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

        message_id = message.reply_message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you called command w\o replied message
    elif message.reply_message is None:
        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)


@bl.chat_message(CommandRuleCustom(ALIASES['unban'], ['!', '/'], 0))
async def unban(message: Message, args: Tuple[str]):
    pass


@bl.chat_message(CommandRuleCustom(ALIASES['unwarn'], ['!', '/'], 1))
async def unwarn(message: Message, args: Tuple[str]):
    pass
