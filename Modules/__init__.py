from . import ForbiddenFilter, MessageQueueHandler, Moderation, ConversationRegistrator, URLFilter

labelers = [ConversationRegistrator.bl, MessageQueueHandler.bl, Moderation.bl, ForbiddenFilter.bl, URLFilter.bl]
