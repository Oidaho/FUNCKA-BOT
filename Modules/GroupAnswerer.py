from vkbottle.bot import Bot, BotLabeler, Message
from Config import TOKEN

bot = Bot(token=TOKEN)
bl = BotLabeler()


@bl.private_message(blocking=False)
async def answer(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer(f'{users_info[0].first_name}, нахуя вы сюда пишите?')


