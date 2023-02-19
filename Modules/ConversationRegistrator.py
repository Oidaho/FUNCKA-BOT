from vkbottle.bot import BotLabeler, Message
from DataBase import DataBaseTools as DBtools

bl = BotLabeler()


@bl.chat_message(
    blocking=False
)
async def check_conversation(message: Message):
    DBtools.add_conversation(message)
