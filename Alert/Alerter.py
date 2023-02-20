from vkbottle.bot import Bot, Message
from Config import GROUP, PERMISSION_LVL, TOKEN

bot = Bot(token=TOKEN)


async def alert_permission_changed(message: Message, users_info, permission_lvl):
    title = f'Группа прав @id{users_info[0].id} (пользователя), ' \
            f'была изменена на {permission_lvl} ({PERMISSION_LVL[str(permission_lvl)]}).'
    await message.answer(title)


async def alert_unbanned(message: Message, uui):
    title = f'С @id{uui[0].id} (пользователя) снята блокировка.\n' \
            f'Теперь он снова может зайти в беседу.'
    await message.answer(title)


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
