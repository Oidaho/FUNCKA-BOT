from vkbottle.bot import Bot, BotLabeler, Message

from Config import GROUP, TOKEN

bot = Bot(token=TOKEN)
bl = BotLabeler()

# TODO: I must try to modify TTF. Right now it's working well, but have small power
forbidden = ['смалкейс', 'сталкейс', 'смал кейс', 'стал кейс', 'черный рынок', 'валюта', ' чр ', 'смоллкеис',
             'смаллкеис', 'еадг', 'фгм', 'клизма', 'катаклизм', 'прожект катаклуcм', 'катаклузм', 'сталкуб', 'сталкубе',
             'смол кеис', 'стол кеис', 'смолкеис']


@bl.chat_message(blocking=False)
async def check_forbidden(message: Message):
    access = True

    for word in forbidden:
        if word in message.text.lower():
            access = False
            break

    if not access:
        # TODO: Make DB request to get current warn count

        warn_count = 0
        title = f'Это слово запрещено.\n' \
                f'@id{message.from_id} (Пользователь) получил предупреждение [{warn_count+1}/3].'
        await message.answer(title)

        await msg_delete(message)

        if warn_count >= 3:
            await call_ban_proc()


async def msg_delete(message: Message):
    message_id = message.conversation_message_id
    await bot.api.messages.delete(group_id=GROUP, peer_id=message.peer_id, cmids=message_id, delete_for_all=True)


async def call_ban_proc():
    pass
    # TODO: BAN
