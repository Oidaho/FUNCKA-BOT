from DataBase import DataBaseTools as DBtools
from vkbottle.bot import Bot
from Config import TOKEN
from Modules import labelers

DBtools.check_db()

bot = Bot(token=TOKEN)

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

bot.run_forever()  # modified
