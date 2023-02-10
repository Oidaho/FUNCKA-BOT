from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()


exclusions = []

forbidden = ['смалкейс', 'сталкейс', 'смал кейс', 'стал кейс', 'черный рынок', 'валюта', ' чр ', 'смоллкейс',
             'смаллкейс', 'еадг', 'фгм', 'клизма', 'катаклизм', 'прожект катаклузм', 'катаклузм', 'сталкуб', 'сталкубе']

aliases = {'а': ['а', 'a', '@'],
           'б': ['б', '6', 'b'],
           'в': ['в', 'b', 'v'],
           'г': ['г', 'r', 'g'],
           'д': ['д', 'd'],
           'е': ['е', 'e', 'ё'],
           'ё': ['ё', 'e'],
           'ж': ['ж', 'zh', 'j'],
           'з': ['з', '3', 'z'],
           'и': ['и', 'u', 'i', 'N', 'й'],
           'й': ['й', 'u', 'i'],
           'к': ['к', 'k', 'i{', '|{'],
           'л': ['л', 'l', 'ji'],
           'м': ['м', 'm'],
           'н': ['н', 'h', 'n'],
           'о': ['о', 'o', '0'],
           'п': ['п', 'n', 'p'],
           'р': ['р', 'r', 'p'],
           'с': ['с', 'c', 's'],
           'т': ['т', 'm', 't'],
           'у': ['у', 'y', 'u'],
           'ф': ['ф', 'f'],
           'х': ['х', 'x', 'h', '}{'],
           'ц': ['ц', 'c', 'u,'],
           'ч': ['ч', 'ch'],
           'ш': ['ш', 'sh'],
           'щ': ['щ', 'sch'],
           'ь': ['ь', 'b'],
           'ы': ['ы', 'bi'],
           'ъ': ['ъ'],
           'э': ['э', 'e'],
           'ю': ['ю', 'io'],
           'я': ['я', 'ya']
           }


def distanceLevenshtein(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


@bl.chat_message(blocking=False)
async def check_forbidden(message: Message):
    access = True
    text = message.text.lower()
    for key, value in aliases.items():
        # Проходимся по каждой букве в значении словаря. То есть по вот этим спискам ['а', 'a', '@'].
        for letter in value:
            # Проходимся по каждой букве в нашей фразе.
            for phr in text:
                # Если буква совпадает с буквой в нашем списке.
                if letter == phr:
                    # Заменяем эту букву на ключ словаря.
                    text = text.replace(phr, key)

    # Проходимся по всем словам.
    for word in forbidden:
        # Разбиваем слово на части, и проходимся по ним.
        for part in range(len(text)):
            # Вот сам наш фрагмент.
            fragment = text[part: part + len(word)]
            # Если отличие этого фрагмента меньше или равно 25% этого слова, то считаем, что они равны.
            if distanceLevenshtein(fragment, word) <= len(word) * 0.10:
                # Если они равны, выводим надпись о их нахождении.
                access = False
                print("Найдено", word, "\nПохоже на", fragment)

    if not access:
        await message.answer(message='Обнаружено запрещенное слово!')