from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()

forbidden = ['смалкеис', 'сталкеис', 'смал кеис', 'стал кеис', 'черный рынок', 'валюта', ' чр ', 'смоллкеис',
             'смаллкеис', 'еадг', 'фгм', 'клизма', 'катаклизм', 'прожект катаклуcм', 'катаклузм', 'сталкуб', 'сталкубе',
             'смол кеис', 'стол кеис', 'смолкеис']


@bl.chat_message(blocking=False)
async def check_forbidden(message: Message):
    access = True

    for word in forbidden:
        if word in message.text:
            access = False

    if not access:
        await message.answer(message='Обнаружено запрещенное слово!')