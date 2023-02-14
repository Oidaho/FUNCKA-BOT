import json
from json import JSONDecodeError
from typing import List


def create_pattern():
    with open("DB.json", "w") as write_file:
        data = {
            'PermanentBanedUsers': List[dict],
            'TempBanedUsers': List[dict],
            'WarnedUsers': List[dict],
            'Permissions': {
                'Moderators': List[dict],
                'Administrators': List[dict],
                'Operators': List[dict]
            },
            'MessageCooldownQueue': List[dict],
        }

        json.dump(data, write_file, indent=4)


def check_db_is_ready():
    try:
        with open("users_data.json", "r") as read_file:
            try:
                json.load(read_file)
                print('DEBUG: DB is ready')

            except JSONDecodeError as error:
                print(error)
                print('DEBUG: Making DB pattern')
                create_pattern()
                print('DEBUG: New DB is ready')

    except FileNotFoundError as error:
        print(error)
        print('DEBUG: Creating DB file and making pattern')
        create_pattern()
        print('DEBUG: New DB is ready')

    return True
