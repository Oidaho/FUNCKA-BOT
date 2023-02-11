from vkbottle import PhotoMessageUploader
from vkbottle.bot import Bot, BotLabeler, Message
from Config import TOKEN

bot = Bot(token=TOKEN)
bl = BotLabeler()
photo_uploader = PhotoMessageUploader(bot.api)


@bl.private_message(blocking=True)
async def answer(message: Message):
    print(message)

    photo = await photo_uploader.upload(
        file_source='Pictures/heh.jpg',
        peer_id=message.peer_id,
    )

    users_info = await bot.api.users.get(message.from_id)

    title = f'@id{users_info[0].id} ({users_info[0].first_name}), сейчас здесь ничего нет, ' \
            f'но и в скором времени тоже не будет!'
    await message.answer(title)

    title = f'Вот Вам анекдот:'
    await message.answer(title)

    title = f'— Дорогой, купи, пожалуйста, батон хлеба, и если будут яйца, возьми десяток.\n' \
            f'Через полчаса муж возвращается домой с десятью батонами. Жена ему говорит:\n' \
            f'— И зачем ты купил столько хлеба??\n' \
            f'— Так ведь яйца-то были...\n' \
            f'\n' \
            f'Комичный элемент в том, что купить он должен был 11 батонов, потому что проверка на яйца идёт после ' \
            f'покупки первого батона, так что муж хуёвый программист.'
    await message.answer(message=title, attachment=photo)
