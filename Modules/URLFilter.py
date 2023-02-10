from vkbottle.bot import BotLabeler, Message
from urlextract import URLExtract

bl = BotLabeler()


@bl.chat_message(blocking=False)
async def check_URL(message: Message):
    extractor = URLExtract()
    if extractor.has_urls(message.text):
        await message.answer(message='Обнаружена ссылка!')
