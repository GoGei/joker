class TelegramIncorrectRecipientException(BaseException):
    """Use when telegram can not identify entry by passed data"""
    pass


class TelegramConnectToBotException(BaseException):
    """Use when telegram API can not connect to bot"""
    pass


class TelegramRecipientNotRegisteredInBotException(BaseException):
    """Use when user does not have conversation with bot"""
    pass


class EmailConnectToMailException(BaseException):
    """Use when django can not connect to email"""
    pass
