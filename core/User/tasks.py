from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from celery_runner import app


@app.task(name='send-activation-link-to-email', ignore_result=True)
def send_activation_link_to_email(user, link, *args, **kwargs):
    base_template = 'User/activation_link.html'
    context = {
        'username': user.username,
        'link': link
    }
    html_message = render_to_string(base_template, context)
    plain_message = strip_tags(html_message)

    subject = 'Activation link'
    sender = settings.DEFAULT_FROM_EMAIL
    recipients = [user.email]

    send_mail(subject, plain_message, sender, recipients, html_message=html_message)
