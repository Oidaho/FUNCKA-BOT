from vkbottle.bot import Bot, BotLabeler, Message
from Config import TOKEN

bot = Bot(token=TOKEN)
bl = BotLabeler()


@bl.chat_message(text=['!бан', '!Бан', '!Ban', '!ban', '!блок', '!Блок'])
async def ban(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.reply(f'{users_info[0].first_name}, к сожалению, команда бана пока что находится в разработке')


@bl.chat_message(text=['!Пред', '!пред', '!Warn', '!warn', '!варн', '!Варн'])
async def warn(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.reply(f'{users_info[0].first_name}, к сожалению, команда предупреждения пока что находится в разработке')
