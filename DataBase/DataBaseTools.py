from vkbottle.bot import Message, Bot
from json import JSONDecodeError
from Config import TOKEN

import time
import json


bot = Bot(token=TOKEN)


def create_pattern():
    with open("DB.json", "w") as write_file:
        pattern = {
            'Conversations': []
        }

        json.dump(pattern, write_file, indent=4)


def check_db():
    try:
        with open("DB.json", "r") as read_file:
            try:
                json.load(read_file)
                print('DEBUG: DB is ready')

            except JSONDecodeError:
                print('WARNING: Data Base file is empty')
                print('DEBUG: Making DB pattern')
                create_pattern()
                print('DEBUG: New DB is ready')

    except FileNotFoundError:
        print('WARNING: Data Base file not found')
        print('DEBUG: Creating DB file and making pattern')
        create_pattern()
        print('DEBUG: New DB is ready')


def add_conversation(message: Message):
    with open("DB.json", "r") as read_file:
        database = json.load(read_file)

    inbase = False

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            inbase = True

    if not inbase:
        conversation_pattern = {
            'PeerID': message.peer_id,
            'PermanentBanedUsers': [],
            'TempBanedUsers': [],
            'WarnedUsers': [],
            'Permissions': {
                'Moderators': [],
                'Administrators': [],
                'Operators': []
            },
            'MessageCooldownQueue': {
                'Cooldown': 0,
                'Queue': []
            },
        }

        database['Conversations'].append(conversation_pattern)

        with open("DB.json", "w") as write_file:
            json.dump(database, write_file, indent=4)


def add_permanent_ban(message: Message):
    with open("DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:

            for user in conversation['PermanentBanedUsers']:
                if user['UserID'] == message.reply_message.from_id:
                    return False

            permanent_ban_pattern = {
                'UserID': message.reply_message.from_id,
                'UserURL': f'https://vk.com/id{message.reply_message.from_id}',
                'BanedByID': message.from_id,
                'BanedByURL': f'https://vk.com/id{message.from_id}'
            }

            conversation['PermanentBanedUsers'].append(permanent_ban_pattern)

            with open("DB.json", "w") as write_file:
                json.dump(database, write_file, indent=4)

            return True


def remove_permanent_ban(message: Message, user_id):
    with open("DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            place = 0
            for user in conversation['PermanentBanedUsers']:
                if user['UserID'] == user_id:
                    conversation['PermanentBanedUsers'].pop(place)

                    with open("DB.json", "w") as write_file:
                        json.dump(database, write_file, indent=4)

                    return True

                place += 1

    return False


def add_temp_ban(message: Message, time, time_type):
    return True


def remove_temp_ban(message: Message):
    pass


def add_warn(message: Message, user_id, warn_count):
    with open("DB.json", "r") as read_file:
        database = json.load(read_file)

    epoch_time = int(time.time())

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            if warn_count == 3:
                place = 0
                for user in conversation['WarnedUsers']:
                    if user['UserID'] == user_id:
                        conversation['WarnedUsers'].pop(place)

                        with open("DB.json", "w") as write_file:
                            json.dump(database, write_file, indent=4)

                        return True

                    place += 1

            elif warn_count == 2:
                for user in conversation['WarnedUsers']:
                    if user['UserID'] == user_id:
                        user['WarnCount'] = warn_count
                        user['LastWarnTime'] = epoch_time
                        user['WarnClearTime'] = epoch_time + (24*60*60)

                        with open("DB.json", "w") as write_file:
                            json.dump(database, write_file, indent=4)

                        return True

            else:
                warn_pattern = {
                        'UserID': user_id,
                        'UserURL': f'https://vk.com/id{user_id}',
                        'WarnCount': warn_count,
                        'LastWarnTime': epoch_time,
                        'WarnClearTime': epoch_time + (24*60*60)
                    }

                conversation['WarnedUsers'].append(warn_pattern)

                with open("DB.json", "w") as write_file:
                    json.dump(database, write_file, indent=4)

                return True

    return False


def get_warn_count(message: Message, user_id):
    with open("DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['WarnedUsers']:
                if user['UserID'] == user_id:
                    return user['WarnCount']

    return 0


def remove_warn(message: Message, user_id, warn_count):
    with open("DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['WarnedUsers']:
                place = 0
                if user['UserID'] == user_id:
                    if warn_count - 1 == 0:
                        conversation['WarnedUsers'].pop(place)

                        with open("DB.json", "w") as write_file:
                            json.dump(database, write_file, indent=4)

                        return True

                    else:
                        user['WarnCount'] = warn_count - 1

                        with open("DB.json", "w") as write_file:
                            json.dump(database, write_file, indent=4)

                        return True

                place += 1

    return False
