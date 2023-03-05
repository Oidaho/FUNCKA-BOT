from vkbottle.bot import Bot, BotLabeler, Message
from Log import Logger as ol
from urlextract import URLExtract
from DataBase import DataBaseTools as DBtools
from Config import GROUP, TOKEN
from Rules.CustomRules import PermissionSelfIgnore, HandleLogConversation

bot = Bot(token=TOKEN)
bl = BotLabeler()

exceptions = [
    'https://forum.exbo.net',
    'https://vk.com/funcka',
    'https://vk.cc/ca5l9d',
    'https://stalcalc.ru',
    'https://vk.cc/c9RYhW',
    'https://vk.com/write-2677092',
    'https://stalcraft.net',
    'https://exbo.net',
    'https://support.exbo.net',
    'https://t.me/stalcraft',
    'https://discord.com/invite/stalcraft',
    'https://store.steampowered.com/app/1818450/STALCRAFT',
    'https://www.twitch.tv/exbo_official',
    'https://www.youtube.com/c/EXBO_official',
    'https://www.tiktok.com/@stalcraft_official',
    'https://www.facebook.com/stalcraft.official',
    'https://twitter.com/STALCRAFT_ENG',
    'https://www.instagram.com/stalcraft_official',
    'https://www.instagram.com/exbo_studio'
 ]


@bl.chat_message(
    HandleLogConversation(False),
    PermissionSelfIgnore(1),
    blocking=False
)
async def check_URL(message: Message):
    if message.deleted is None:

        extractor = URLExtract()

        if extractor.has_urls(message.text):
            found = False

            for url in exceptions:
                if message.text.startswith(url):
                    found = True

            if not found:
                mute_users_info = await bot.api.users.get(message.from_id)

                message_id = message.conversation_message_id
                await bot.api.messages.delete(
                    group_id=GROUP,
                    peer_id=message.peer_id,
                    cmids=message_id,
                    delete_for_all=True
                )
                message.deleted = True

                time_value = '1'
                time_type = 'hour(s)'

                reason = 'Внешние ссылки'

                await ol.log_system_muted(message, mute_users_info, time_value, time_type, reason)

                title = f'Подозрительная активность @id{mute_users_info[0].id} (участника) (Внешние ссылки)\n'\
                        f'@id{mute_users_info[0].id} (Пользователь) ' \
                        f'был заглушен на {time_value} {time_type} в целях безопасности.'
                await message.answer(title)

                DBtools.add_mute(message, message.from_id, time_value, time_type)
