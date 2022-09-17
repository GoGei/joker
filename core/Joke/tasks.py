from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from premailer import transform

from celery_runner import app


@app.task(ignore_result=True, name='send-joke-to-email')
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
