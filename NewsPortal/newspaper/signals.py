import json
import os

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from newspaper.views import Post
from django.template.loader import render_to_string


@receiver(post_save, sender=Post)
def created_handler(sender, instance, created, **kwargs):
    instance_category = instance.category.first()

    if instance_category and not created:
        post_id = instance.pk
        emails_in_dict = instance_category.users.all().values('email')
        emails = []

        for user_email in emails_in_dict:
            emails.append(user_email['email'])

        html = render_to_string(
            'newspaper/send_messages/message.html',
            {'post_id': post_id},
        )

        msg = EmailMultiAlternatives(
                subject=f'Добавлен новый товар по категории "{instance_category}"',
                from_email='pten4ik99@yandex.ru',
                to=emails
            )

        msg.attach_alternative(html, 'text/html')
        msg.send()