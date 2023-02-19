from . import ForbiddenFilter, URLFilter, MessageQueueHandler, Moderation, ConversationRegistrator

labelers = [ConversationRegistrator.bl, MessageQueueHandler.bl, Moderation.bl, ForbiddenFilter.bl, URLFilter.bl]
