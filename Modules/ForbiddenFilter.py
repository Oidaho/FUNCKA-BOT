from vkbottle.bot import Bot, BotLabeler, Message
from Config import GROUP, TOKEN
from DataBase import DataBaseTools as DBtools
from Log import Logger as ol
from Rules.CustomRules import PermissionSelfIgnore, HandleLogConversation

bot = Bot(token=TOKEN)
bl = BotLabeler()

forbidden = [
    'смалкейс', 'смал кейс', 'смаллкейс', 'смалл кейс' 'смолкейс', 'смоллкейс', 'смолл кейс', 'смол кейс',
    'смалкеис', 'смал кеис', 'смаллкеис', 'смалл кеис' 'смолкеис', 'смоллкеис', 'смолл кеис', 'смол кеис',
    'сталкейс', 'стал кейс', 'стол кейс', 'столкейс', 'сталл кейс', 'черный рынок', 'валюта', ' чр ',
    'еадг', 'фгм', 'клизма', 'катаклизм', 'прожект катаклизм', 'катакизм', 'сталкуб', 'сталкубе',
]


@bl.chat_message(
    HandleLogConversation(False),
    PermissionSelfIgnore(1),
    blocking=False
)
async def check_forbidden(message: Message):
    if message.deleted is None:

        spotted = False
        reason = 'Неизвестно'

        if not spotted:
            for word in forbidden:
                if word in message.text.lower():
                    spotted = True
                    reason = 'Нежелательное слово'
                    break

        if not spotted and not DBtools.get_setting(message, 'Allow_Picture'):
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.photo is not None:
                        spotted = True
                        reason = 'Вложенная фотография'
                        break

        if not spotted and not DBtools.get_setting(message, 'Allow_Video'):
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.video is not None:
                        spotted = True
                        reason = 'Вложенное видео'
                        break

        if not spotted and not DBtools.get_setting(message, 'Allow_Music'):
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.audio is not None:
                        spotted = True
                        reason = 'Вложенная музыка'
                        break

        if not spotted and not DBtools.get_setting(message, 'Allow_Voice'):
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.audio_message is not None:
                        spotted = True
                        reason = 'Голосовое сообщение'
                        break

        if not spotted and not DBtools.get_setting(message, 'Allow_Post'):
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.wall_reply is not None or attachment.wall is not None:
                        spotted = True
                        reason = 'Репост'
                        break

        if not spotted and not DBtools.get_setting(message, 'Allow_Votes'):
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.poll is not None:
                        spotted = True
                        reason = 'Вложенное голосование'
                        break

        if not spotted and not DBtools.get_setting(message, 'Allow_Files'):
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.doc is not None:
                        spotted = True
                        reason = 'Вложенный файл'
                        break

        if not spotted and not DBtools.get_setting(message, 'Allow_Miniapp'):
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.mini_app is not None:
                        spotted = True
                        reason = 'Вложенное мини-приложение'
                        break

        if not spotted and not DBtools.get_setting(message, 'Allow_Graffiti'):
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.graffiti is not None:
                        spotted = True
                        reason = 'Граффити'
                        break

        if not spotted and not DBtools.get_setting(message, 'Allow_Sticker'):
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.sticker is not None:
                        spotted = True
                        reason = 'Стикер'
                        break

        if spotted:
            warn_users_info = await bot.api.users.get(message.from_id)
            warn_count = DBtools.get_warn_count(message, message.from_id)

            title = f'Этот контент ({reason}) запрещен в данной беседе.\n' \
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
            message.deleted = True

            DBtools.add_warn(message, message.from_id, warn_count + 1)

            if warn_count + 1 == 3:
                reason = 'Получено 3 предупреждения'
                mute_users_info = await bot.api.users.get(message.from_id)

                time = '3'
                time_type = 'day(s)'

                if DBtools.add_mute(message, message.from_id, time, time_type):
                    title = f'@id{mute_users_info[0].id} (Пользователь) ' \
                            f'был заглушен на {time} {time_type}.'
                    await message.answer(title)
                    await ol.log_system_muted(message, mute_users_info, time, time_type, reason)
