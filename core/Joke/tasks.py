import smtplib

from django.conf import settings
from django.core.mail import send_mail
from telethon import TelegramClient, sync
from telethon.errors import rpcerrorlist as telegram_errors
from celery_runner import app
from . import exceptions
from . import enums


@app.task(name='send-joke-to-email')
def send_joke_to_email(joke, recipient, *args, **kwargs):
    html_message = joke.prepared_html_message
    plain_message = joke.prepared_plain_message

    subject = 'This is a joke!'
    sender = settings.DEFAULT_FROM_EMAIL
    recipients = [recipient]

    try:
        send_mail(subject, plain_message, sender, recipients, html_message=html_message)
    except smtplib.SMTPAuthenticationError as e:
        raise exceptions.EmailConnectToMailException()

    return True, None


@app.task(name='send-joke-to-telegram')
def send_joke_to_telegram(joke, recipient):
    api_id = settings.TELEGRAM_API_KEY
    api_hash = settings.TELEGRAM_API_HASH
    bot_token = settings.TELEGRAM_BOT_TOKEN

    client = TelegramClient(settings.TELEGRAM_SESSION_STORAGE_NAME, api_id, api_hash)

    try:
        client.start(bot_token=bot_token)
        entity = client.get_entity(recipient)
        html_message = joke.prepared_html_message
        sync.syncify(client.send_message(entity=entity, message=html_message, parse_mode='html'))
    except (ValueError, telegram_errors.PeerIdInvalidError) as e:
        raise exceptions.TelegramRecipientNotRegisteredInBotException()
    except telegram_errors.UsernameInvalidError as e:
        raise exceptions.TelegramIncorrectRecipientException()
    except (telegram_errors.ApiIdInvalidError, telegram_errors.AccessTokenInvalidError) as e:
        raise exceptions.TelegramConnectToBotException()
    finally:
        client.disconnect()

    return True, None


@app.task(name='send-daily-jokes')
def send_daily_jokes_to_users(send_method: enums.SendMethods):
    from random import randint
    from core.Joke.models import Joke
    from core.User.models import User

    def get_random_joke_from_qs(qs):
        if qs.exists():
            return queryset[randint(0, qs.count() - 1)]
        return None

    def perform_send(func, *args, **kwargs):
        try:
            is_send, result = func(*args, **kwargs)
            if is_send:
                joke.make_seen(user)
        except Exception as e:
            print(e)

    queryset = Joke.objects.prefetch_related('jokeseen_set', 'jokelikestatus_set')

    users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False)
    for user in users:
        jokes = Joke.get_unseen_jokes(user)

        if not jokes.exists():
            Joke.clear_seen_jokes(user)
            jokes = Joke.get_unseen_jokes(user)

        joke = get_random_joke_from_qs(jokes)
        if joke:
            if send_method == enums.SendMethods.EMAIL:
                perform_send(joke.send_to_email, (user.email,))
            elif send_method == enums.SendMethods.TELEGRAM_BOT:
                perform_send(joke.send_to_telegram_username, (user.tg_nickname,))
            else:
                raise exceptions.InvalidSendMethod()

    return True
