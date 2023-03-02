from vkbottle.bot import Bot, BotLabeler, Message

from Config import TOKEN, GROUP
from DataBase import DataBaseTools as DBtools
from Log import Logger as ol
from Rules.CustomRules import PermissionSelfIgnore, HandleLogConversation

bot = Bot(token=TOKEN)
bl = BotLabeler()


@bl.chat_message(
    PermissionSelfIgnore(1),
    HandleLogConversation(False),
    blocking=False
)
async def add_to_message_queue(message: Message):
    if DBtools.check_mute(message, message.from_id):
        reason = 'Нарушено заглушение'

        mute_users_info = await bot.api.users.get(message.from_id)

        time = '3'
        time_type = 'day(s)'

        if DBtools.add_temp_ban(message, message.from_id, time, time_type):
            title = f'@id{mute_users_info[0].id} (Пользователь) ' \
                    f'был заблокирован на {time} {time_type}.'
            await message.answer(title)
            await ol.log_system_banned(message, mute_users_info, time, time_type, reason)

            await bot.api.messages.remove_chat_user(message.chat_id, message.from_id)

    elif DBtools.get_cooldown(message) != 0:
        if DBtools.check_message_queue(message):
            DBtools.add_to_message_queue(message)

        else:
            warn_users_info = await bot.api.users.get(message.from_id)
            warn_count = DBtools.get_warn_count(message, message.from_id)

            reason = 'Нарушение задержки'

            title = f'Остынь! Соблюдай медленный режим.\n' \
                    f'@id{message.from_id} (Пользователь) получил предупреждение [{warn_count + 1}/3].'
            await message.answer(title)
            await ol.log_system_warned(message, warn_users_info, warn_count + 1, reason)
            message_id = message.conversation_message_id
            await bot.api.messages.delete(
                group_id=GROUP,
                peer_id=message.peer_id,
                cmids=message_id,
                delete_for_all=True
            )

            DBtools.add_warn(message, message.from_id, warn_count + 1)

            if warn_count + 1 == 3:
                reason = 'Получено 3 предупреждения'
                mute_users_info = await bot.api.users.get(message.from_id)

                time = '1'
                time_type = 'day(s)'

                if DBtools.add_mute(message, message.from_id, time, time_type):
                    title = f'@id{mute_users_info[0].id} (Пользователь) ' \
                            f'был заглушен на {time} {time_type}.'
                    await message.answer(title)
                    await ol.log_system_muted(message, mute_users_info, time, time_type, reason)
