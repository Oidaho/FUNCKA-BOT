from typing import List, Optional, Union
from urlextract import URLExtract
from vkbottle import ABCRule, Bot
from DataBase import DataBaseTools as DBtools
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from Config import GROUP, TOKEN

bot = Bot(token=TOKEN)

DEFAULT_PREFIXES = ["!", "/"]
DEFAULT_ALIASES = ["Command", "command"]
STANDARD_PERMISSION = 1
STANDARD_REPLY = False
STANDARD_LOG_HANDLE = False


class HandleCommand(ABCRule[BaseMessageMin]):

    def __init__(
            self,
            command_aliases: Optional[List[str]] = None,
            prefixes: Optional[List[str]] = None,
            args_count: int = 0
    ):
        self.prefixes = prefixes or DEFAULT_PREFIXES
        self.command_aliases = command_aliases or DEFAULT_ALIASES
        self.args_count = args_count
        self.sep = " "

    async def check(self, message: BaseMessageMin) -> Union[dict, bool]:
        text = message.text

        # Тут игнорируются аргументы, если команда имеет 0 аргументов в настройке
        if not self.args_count and self.sep in text:
            cut = message.text.find(self.sep)
            text = text[0:cut]

        for prefix in self.prefixes:
            for command_text in self.command_aliases:
                command_length = len(prefix + command_text)
                command_length_with_sep = command_length + len(self.sep)
                if text.startswith(prefix + command_text):
                    # Если команда имеет 0 аргументов в настройке
                    if not self.args_count and len(text) == command_length:
                        try:
                            await bot.api.messages.delete(
                                group_id=GROUP,
                                peer_id=message.peer_id,
                                cmids=message.conversation_message_id,
                                delete_for_all=True
                            )
                        except Exception:
                            pass

                        return True

                    elif self.args_count:
                        args = message.text[command_length_with_sep:].split(self.sep)
                        if len(args) == self.args_count and all(args):
                            try:
                                await bot.api.messages.delete(
                                    group_id=GROUP,
                                    peer_id=message.peer_id,
                                    cmids=message.conversation_message_id,
                                    delete_for_all=True
                                )
                            except Exception:
                                pass

                            return {"args": args}

                        else:
                            print('deleted')
                            try:
                                await bot.api.messages.delete(
                                    group_id=GROUP,
                                    peer_id=message.peer_id,
                                    cmids=message.conversation_message_id,
                                    delete_for_all=True
                                )
                            except Exception:
                                pass

                            return False

        return False


class PermissionAccess(ABCRule[BaseMessageMin]):
    def __init__(self, accessed_lvl: Optional[int] = None):
        self.accessed_lvl = accessed_lvl or STANDARD_PERMISSION

    async def check(self, message: BaseMessageMin) -> bool:
        members = await bot.api.messages.get_conversation_members(group_id=GROUP, peer_id=message.peer_id)
        members = members.items
        for member in members:
            if member.member_id == message.from_id and member.is_admin:
                return True

        user_permission = DBtools.get_permission(message, message.from_id)

        if user_permission >= self.accessed_lvl:
            return True

        else:
            return False


class PermissionIgnore(ABCRule[BaseMessageMin]):
    def __init__(self, ignore_lvl: Optional[int] = None):
        self.ignore_lvl = ignore_lvl or STANDARD_PERMISSION
        self.sep = " "

    async def check(self, message: BaseMessageMin) -> bool:
        if message.reply_message is not None:
            target_user_id = message.reply_message.from_id
            target_user_permission = DBtools.get_permission(message, target_user_id)
            if target_user_permission < self.ignore_lvl:
                return True

            else:
                return False

        elif message.fwd_messages:
            if all([DBtools.get_permission(msg, msg.from_id) < self.ignore_lvl for msg in message.fwd_messages]):
                return True

            else:
                return False

        else:
            text = message.text
            if self.sep in text:
                cut = text.find(self.sep)
                text = text[cut:]
                args = text.split(self.sep)
                extractor = URLExtract()
                for arg in args:
                    print(arg)
                    if extractor.has_urls(arg):
                        if arg.startswith('https://vk.com/id'):
                            shortname = int(arg.replace('https://vk.com/id', ''))
                            users_info = await bot.api.users.get([shortname])
                            user_permission = DBtools.get_permission(message, users_info[0].id)
                            if user_permission < self.ignore_lvl:
                                return True

                            else:
                                return False

                        elif arg.startswith('https://vk.com/'):
                            shortname = arg.replace('https://vk.com/', '')
                            users_info = await bot.api.users.get([shortname])
                            user_permission = DBtools.get_permission(message, users_info[0].id)
                            if user_permission < self.ignore_lvl:
                                return True

                            else:
                                return False

            return True


class PermissionSelfIgnore(ABCRule[BaseMessageMin]):
    def __init__(self, ignore_lvl: Optional[int] = None):
        self.ignore_lvl = ignore_lvl or STANDARD_PERMISSION
        self.sep = " "

    async def check(self, message: BaseMessageMin) -> bool:
        user_permission = DBtools.get_permission(message, message.from_id)
        if user_permission >= self.ignore_lvl:
            return False

        else:
            return True


class HandleRepliedMessages(ABCRule[BaseMessageMin]):
    def __init__(self, handle_reply: Optional[bool] = None):
        self.handle_reply = handle_reply or STANDARD_REPLY

    async def check(self, message: BaseMessageMin) -> bool:
        if self.handle_reply:
            if message.reply_message is not None or message.fwd_messages:
                return True

            else:
                return False

        else:
            if message.reply_message is not None or message.fwd_messages:
                return False

            else:
                return True


class HandleLogConversation(ABCRule[BaseMessageMin]):
    def __init__(self, handle_log: Optional[bool] = None):
        self.handle_log = handle_log or STANDARD_LOG_HANDLE

    async def check(self, message: BaseMessageMin) -> bool:
        if self.handle_log:
            return True

        else:
            log_peer = DBtools.get_log_conversation()
            if message.peer_id == log_peer:
                return False

            else:
                return True
