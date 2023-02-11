from vkbottle.bot import Bot, BotLabeler, Message
from Config import TOKEN

bot = Bot(token=TOKEN)
bl = BotLabeler()

# TODO: Think of the best way to respond to private messages in public
@bl.private_message(blocking=False)
async def answer(message: Message):
    users_info = await bot.api.users.get(message.from_id)

    title = f'{users_info[0].first_name}, сейчас здесь ничего нет, но в скором времени обязательно появится!'
    await message.answer(title)


