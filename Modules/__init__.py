from . import (
    ForbiddenFilter,
    MessageQueueHandler,
    Moderation,
    ConversationRegistrator,
    URLFilter,
    AccAgeChecker
)

labelers = [
    ConversationRegistrator.bl,
    AccAgeChecker.bl,
    MessageQueueHandler.bl,
    Moderation.bl,
    ForbiddenFilter.bl,
    URLFilter.bl
]
