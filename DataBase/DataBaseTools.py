from vkbottle.bot import Message, Bot
from json import JSONDecodeError
from Config import TOKEN

import time
import json


bot = Bot(token=TOKEN)


def create_pattern():
    with open("DataBase/DB.json", "w") as write_file:
        pattern = {
            'Conversations': []
        }

        json.dump(pattern, write_file, indent=4)


def check_db():
    try:
        with open("DataBase/DB.json", "r") as read_file:
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
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    inbase = False

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            inbase = True

    if not inbase:
        conversation_pattern = {
            'PeerID': message.peer_id,
            'PermanentBannedUsers': [],
            'TempBannedUsers': [],
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

        with open("DataBase/DB.json", "w") as write_file:
            json.dump(database, write_file, indent=4)


def add_permanent_ban(message: Message):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:

            for user in conversation['PermanentBannedUsers']:
                if user['UserID'] == message.reply_message.from_id:
                    return False

            permanent_ban_pattern = {
                'UserID': message.reply_message.from_id,
                'UserURL': f'https://vk.com/id{message.reply_message.from_id}',
                'BannedByID': message.from_id,
                'BannedByURL': f'https://vk.com/id{message.from_id}'
            }

            conversation['PermanentBannedUsers'].append(permanent_ban_pattern)

            with open("DataBase/DB.json", "w") as write_file:
                json.dump(database, write_file, indent=4)

            return True


def remove_permanent_ban(message: Message, user_id):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            place = 0
            for user in conversation['PermanentBannedUsers']:
                if user['UserID'] == user_id:
                    conversation['PermanentBannedUsers'].pop(place)

                    with open("DataBase/DB.json", "w") as write_file:
                        json.dump(database, write_file, indent=4)

                    return True

                place += 1

    return False


def add_temp_ban(message: Message, user_id, current_time, time_type):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    epoch_time = int(time.time())

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['TempBannedUsers']:
                if user['UserID'] == user_id:
                    return False
            modify = 1

            if time_type == 'month(s)':
                modify = 31 * 24 * 60 * 60
            if time_type == 'day(s)':
                modify = 24 * 60 * 60
            if time_type == 'hour(s)':
                modify = 60 * 60

            summary_time = int(current_time) * modify

            temp_ban_pattern = {
                        'UserID': user_id,
                        'UserURL': f'https://vk.com/id{user_id}',
                        'BannedByID': message.from_id,
                        'BannedByURL': f'https://vk.com/id{message.from_id}',
                        'BanTime': epoch_time,
                        'BanClearTime': epoch_time + summary_time
                    }

            conversation['TempBannedUsers'].append(temp_ban_pattern)

            with open("DataBase/DB.json", "w") as write_file:
                json.dump(database, write_file, indent=4)

            return True

    return False


def remove_temp_ban(message: Message, user_id):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            place = 0
            for user in conversation['TempBannedUsers']:
                if user['UserID'] == user_id:
                    conversation['TempBannedUsers'].pop(place)

                with open("DataBase/DB.json", "w") as write_file:
                    json.dump(database, write_file, indent=4)

                return True

            place += 1

    return False


def add_warn(message: Message, user_id, warn_count):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    epoch_time = int(time.time())

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            if warn_count == 3:
                place = 0
                for user in conversation['WarnedUsers']:
                    if user['UserID'] == user_id:
                        conversation['WarnedUsers'].pop(place)

                        with open("DataBase/DB.json", "w") as write_file:
                            json.dump(database, write_file, indent=4)

                        return True

                    place += 1

            elif warn_count == 2:
                for user in conversation['WarnedUsers']:
                    if user['UserID'] == user_id:
                        user['WarnCount'] = warn_count
                        user['LastWarnTime'] = epoch_time
                        user['WarnClearTime'] = epoch_time + (24*60*60)

                        with open("DataBase/DB.json", "w") as write_file:
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

                with open("DataBase/DB.json", "w") as write_file:
                    json.dump(database, write_file, indent=4)

                return True

    return False


def remove_warn(message: Message, user_id, warn_count):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['WarnedUsers']:
                place = 0
                if user['UserID'] == user_id:
                    if warn_count - 1 == 0:
                        conversation['WarnedUsers'].pop(place)

                        with open("DataBase/DB.json", "w") as write_file:
                            json.dump(database, write_file, indent=4)

                        return True

                    else:
                        user['WarnCount'] = warn_count - 1

                        with open("DataBase/DB.json", "w") as write_file:
                            json.dump(database, write_file, indent=4)

                        return True

                place += 1

    return False


def get_warn_count(message: Message, user_id):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['WarnedUsers']:
                if user['UserID'] == user_id:
                    return user['WarnCount']

    return 0


def get_ban_kind(message: Message, user_id):
    with open("DataBase/DB.json", "r") as read_file:
        database = json.load(read_file)

    for conversation in database['Conversations']:
        if conversation['PeerID'] == message.peer_id:
            for user in conversation['TempBannedUsers']:
                if user['UserID'] == user_id:
                    return 'temp'

            for user in conversation['PermanentBannedUsers']:
                if user['UserID'] == user_id:
                    return 'permanent'

    return None
