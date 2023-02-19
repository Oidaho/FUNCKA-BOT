from vkbottle.bot import Bot, BotLabeler, Message

from Config import TOKEN, GROUP
from DataBase import DataBaseTools as DBtools
from Rules.CustomRules import PermissionSelfIgnore, HandleLogConversation

bot = Bot(token=TOKEN)
bl = BotLabeler()


@bl.chat_message(
    PermissionSelfIgnore(1),
    HandleLogConversation(False),
    blocking=False
)
async def add_to_message_queue(message: Message):
    if DBtools.get_cooldown(message) != 0:
        if DBtools.check_message_queue(message):
            DBtools.add_to_message_queue(message)

        else:
            warn_count = DBtools.get_warn_count(message, message.from_id)

            title = f'Это слово запрещено.\n' \
                    f'@id{message.from_id} (Пользователь) получил предупреждение [{warn_count + 1}/3].'
            await message.answer(title)
            await self_msg_delete(message)

            DBtools.add_warn(message, message.from_id, warn_count + 1)

            if warn_count + 1 == 3:
                await call_ban_proc(message)


'''
-----------------------------------------------------------------------------------------------------------------------
'''


async def call_ban_proc(message: Message):
    ban_users_info = await bot.api.users.get(message.from_id)

    time = '3'
    time_type = 'day(s)'

    title = f'@id{ban_users_info[0].id} (Пользователь) ' \
            f'был заблокирован на {time} {time_type}.'
    await message.answer(title)

    DBtools.add_temp_ban(message, message.from_id, time, time_type)

    '''await bot.api.messages.remove_chat_user(message.reply_message.from_id)'''


async def self_msg_delete(message: Message):
    message_id = message.conversation_message_id
    await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)
