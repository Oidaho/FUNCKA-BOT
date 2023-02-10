from vkbottle.bot import Bot, BotLabeler, Message
from vkbottle.dispatch.rules.base import CommandRule
from typing import Tuple

from Config import TOKEN

bot = Bot(token=TOKEN)
bl = BotLabeler()

ban_type = {
    'h': 'hour(s)',
    'd': 'day(s)',
    'm': 'month(s)',
    'p': 'permanent'
}


@bl.chat_message(CommandRule('ban', ['!', '/'], 2))
async def ban(message: Message, args: Tuple[str]):
    if (message.reply_message is not None) and (message.reply_message.from_id != message.from_id):
        users_info = await bot.api.users.get(message.from_id)
        ban_user_info = await bot.api.users.get(message.reply_message.from_id)

        await message.reply(f'{users_info[0].first_name}, к сожалению, команда бана пока что находится в разработке')

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

        await message.answer(f'Но если бы бан работал, то {ban_user_info[0].first_name} был бы забанен на {time} {time_type}')

        message_id = message.reply_message.conversation_message_id
        group_id = 218730916
        await bot.api.messages.delete(peer_id=message.peer_id, cmids=message_id, delete_for_all=True,
                                      group_id=group_id)
        message_id = message.conversation_message_id
        await bot.api.messages.delete(peer_id=message.peer_id, cmids=message_id, delete_for_all=True,
                                      group_id=group_id)


    elif message.reply_message.from_id == message.from_id:
        users_info = await bot.api.users.get(message.from_id)
        await message.reply(f'{users_info[0].first_name}, нельзя применить команду к себе.')

        message_id = message.reply_message.conversation_message_id
        group_id = 218730916
        await bot.api.messages.delete(peer_id=message.peer_id, cmids=message_id, delete_for_all=True,
                                      group_id=group_id)
        message_id = message.conversation_message_id
        await bot.api.messages.delete(peer_id=message.peer_id, cmids=message_id, delete_for_all=True,
                                      group_id=group_id)


@bl.chat_message(CommandRule('warn', ['!', '/'], 0))
async def warn(message: Message):
    if (message.reply_message is not None) and (message.reply_message.from_id != message.from_id):
        users_info = await bot.api.users.get(message.from_id)
        warn_user_info = await bot.api.users.get(message.reply_message.from_id)
        await message.reply(f'{users_info[0].first_name}, к сожалению, команда предупреждения пока что находится в разработке')
        await message.answer(f'Но если бы предупреждение работало, то {warn_user_info[0].first_name} получил бы предупреждение')

        message_id = message.reply_message.conversation_message_id
        group_id = 218730916
        await bot.api.messages.delete(peer_id=message.peer_id, cmids=message_id, delete_for_all=True,
                                      group_id=group_id)
        message_id = message.conversation_message_id
        await bot.api.messages.delete(peer_id=message.peer_id, cmids=message_id, delete_for_all=True,
                                      group_id=group_id)

    elif message.reply_message.from_id == message.from_id:
        users_info = await bot.api.users.get(message.from_id)
        await message.reply(f'{users_info[0].first_name}, нельзя применить команду к себе.')

        message_id = message.reply_message.conversation_message_id
        group_id = 218730916
        await bot.api.messages.delete(peer_id=message.peer_id, cmids=message_id, delete_for_all=True,
                                      group_id=group_id)
        message_id = message.conversation_message_id
        await bot.api.messages.delete(peer_id=message.peer_id, cmids=message_id, delete_for_all=True,
                                      group_id=group_id)
