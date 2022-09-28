class TelegramIncorrectRecipientException(Exception):
    """Use when telegram can not identify entry by passed data"""
    pass


class TelegramConnectToBotException(Exception):
    """Use when telegram API can not connect to bot"""
    pass


class TelegramRecipientNotRegisteredInBotException(Exception):
    """Use when user does not have conversation with bot"""
    pass


class EmailConnectToMailException(Exception):
    """Use when django can not connect to email"""
    pass


class InvalidSendMethod(Exception):
    """Use when method of joke send is unknown"""
    pass
