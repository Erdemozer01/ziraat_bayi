import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def email_sender(subject, sender, recipients, template, context):
    template_name = os.path.join(BASE_DIR, 'templates', 'emails', '%s.html' % template)

    html_content = render_to_string(
        template_name=str(template_name),
        context=context,
    )

    msg = EmailMultiAlternatives(subject, html_content, sender, [recipients])
    msg.content_subtype = "html"

    return msg.send()
