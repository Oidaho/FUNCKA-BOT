from vkbottle.bot import Bot, BotLabeler, Message
from urlextract import URLExtract

from Config import TOKEN, GROUP

bot = Bot(token=TOKEN)
bl = BotLabeler()


@bl.chat_message(blocking=False)
async def check_URL(message: Message):
    extractor = URLExtract()
    if extractor.has_urls(message.text):
        users_info = await bot.api.users.get(message.from_id)

        title = f'Подозрительная активность @id{users_info[0].id} (участника) (Внешние ссылки).' \
                f'\nБлокировка на 1 час в целях безопасности.'
        await message.answer(title)

        # TODO: 1 hour ban procedure somewhere

        message_id = message.conversation_message_id
        await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)

