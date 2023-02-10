from vkbottle.bot import Bot, BotLabeler, Message
from vkbottle.dispatch.rules.base import CommandRule

from Config import TOKEN

bot = Bot(token=TOKEN)
bl = BotLabeler()


@bl.chat_message(CommandRule("ban", ["!", "/"], 2))
async def ban(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.reply(f'{users_info[0].first_name}, к сожалению, команда бана пока что находится в разработке')


@bl.chat_message(CommandRule("warn", ["!", "/"], 2))
async def warn(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.reply(f'{users_info[0].first_name}, к сожалению, команда предупреждения пока что находится в разработке')
