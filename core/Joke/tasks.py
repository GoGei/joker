import smtplib

from django.conf import settings
from django.core.mail import send_mail
from telethon import TelegramClient, sync, errors

from celery_runner import app


@app.task(name='send-joke-to-email')
def send_joke_to_email(joke, recipient, *args, **kwargs):
    html_message = joke.prepared_html_message
    plain_message = joke.prepared_plain_message

    subject = 'This is a joke!'
    sender = settings.DEFAULT_FROM_EMAIL
    recipients = [recipient]

    try:
        send_mail(subject, plain_message, sender, recipients, html_message=html_message)
    except smtplib.SMTPAuthenticationError:
        return False, 'Login not successful'
    except Exception:
        return False, 'Something went wrong'

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
    except ValueError as e:
        return False, str(e)
    except (errors.rpcerrorlist.ApiIdInvalidError, errors.rpcerrorlist.AccessTokenInvalidError) as e:
        return False, 'Login not successful'
    except Exception:
        return False, 'Something went wrong'
    finally:
        client.disconnect()

    return True, None
