from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from telethon import TelegramClient, sync, errors

from celery_runner import app


@app.task(name='send-joke-to-email')
def send_joke_to_email(joke, recipient, *args, **kwargs):
    base_template = 'core_templates/joke_email.html'
    context = {'joke_text': joke.text}

    html_message = render_to_string(base_template, context)
    plain_message = strip_tags(html_message)

    subject = 'This is a joke!'
    sender = settings.DEFAULT_FROM_EMAIL
    recipients = [recipient]

    send_mail(subject, plain_message, sender, recipients, html_message=html_message)
    return True


@app.task(name='send-joke-to-telegram')
def send_joke_to_telegram(joke, recipient):
    base_template = 'core_templates/joke_email.html'
    context = {'joke_text': joke.text}
    api_id = settings.TELEGRAM_API_KEY
    api_hash = settings.TELEGRAM_API_HASH
    bot_token = settings.TELEGRAM_BOT_TOKEN

    html_message = render_to_string(base_template, context)
    client = TelegramClient(settings.TELEGRAM_SESSION_STORAGE_NAME, api_id, api_hash)

    try:
        client.start(bot_token=bot_token)
        entity = client.get_entity(recipient)
        sync.syncify(client.send_message(entity=entity, message=html_message, parse_mode='html'))
    except (ValueError, errors.PeerIdInvalidError) as e:
        print(e)
        return False
    finally:
        client.disconnect()

    return True
