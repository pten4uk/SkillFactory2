import json
import os
from datetime import timedelta, datetime

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from newspaper.views import Post
from django.template.loader import render_to_string


@receiver(post_save, sender=Post)
def created_handler(sender, instance, **kwargs):
    instance_category = instance.category.all()

    for cat in instance_category:
        if os.path.exists('subscribers.json'):
            with open('subscribers.json', 'r', encoding='utf8') as f:
                categories_in_db = json.load(f)
            emails = []
            for category in categories_in_db:
                if category == cat.name:
                    emails = categories_in_db[category]
                    break

            post_id = instance.pk
            html = render_to_string(
                'newspaper/message.html',
                {'post_id': post_id},
            )

            msg = EmailMultiAlternatives(
                    subject=f'Добавлен новый товар по категории "{cat.name}"',
                    from_email='pten4ik99@yandex.ru',
                    to=emails
                )

            msg.attach_alternative(html, 'text/html')
            msg.send()