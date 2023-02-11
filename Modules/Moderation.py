from vkbottle.bot import Bot, BotLabeler, Message
from vkbottle.dispatch.rules.base import CommandRule
from typing import Tuple

from Config import TOKEN, GROUP, ban_type

import asyncio

bot = Bot(token=TOKEN)
bl = BotLabeler()


async def ban_user():
    pass


async def warn_user():
    pass


@bl.chat_message(CommandRule('ban', ['!', '/'], 2))
async def ban(message: Message, args: Tuple[str]):
    # if you want to ban something user
    if (message.reply_message is not None) and (message.reply_message.from_id != message.from_id):
        ban_users_info = await bot.api.users.get(message.reply_message.from_id)

        time = args[0]
        time_type = ban_type[args[1]]

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
            time_type = ban_type['d']

        title = f'Пользователь @id{ban_users_info[0].id} ({ban_users_info[0].first_name}) был заблокирован на {time} {time_type}.'
        await message.answer(title)

        # Ban procedure somewhere

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

        message_id = message.reply_message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you want to ban yourself
    elif message.reply_message.from_id == message.from_id:
        users_info = await bot.api.users.get(message.from_id)

        title = f'@id{users_info[0].id} ({users_info[0].first_name}), нельзя применить команду к своему сообщению.'
        await message.answer(title)

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

        message_id = message.reply_message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)


@bl.chat_message(CommandRule('warn', ['!', '/'], 0))
async def warn(message: Message):
    # if you want to warn something user
    if (message.reply_message is not None) and (message.reply_message.from_id != message.from_id):
        warn_users_info = await bot.api.users.get(message.reply_message.from_id)

        title = f'Пользователь @id{warn_users_info[0].id} ({warn_users_info[0].first_name}) получил предупреждение [0/3].'
        await message.answer(title)

        # Warn procedure somewhere

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

        message_id = message.reply_message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

    # if you want to warn yourself
    elif message.reply_message.from_id == message.from_id:
        users_info = await bot.api.users.get(message.from_id)

        title = f'@id{users_info[0].id} ({users_info[0].first_name}), нельзя применить команду к своему сообщению.'
        await message.answer(title)

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

        message_id = message.reply_message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)
