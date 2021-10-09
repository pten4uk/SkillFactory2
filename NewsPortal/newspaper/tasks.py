import json
import os
from datetime import datetime, timedelta

from NewsPaper.models import Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from celery import shared_task


@shared_task
def mail_sender():
    if os.path.exists('subscribers.json'):
        with open('subscribers.json', 'r', encoding='utf8') as f:
            info = json.load(f)
        post_list = Post.objects.filter(datetime__range=[datetime.now() - timedelta(days=7), datetime.now()])

        for cat, emails in info.items():
            if emails:
                html = render_to_string(
                    'newspaper/sender_mail.html',
                    {
                        'post_list': post_list,
                    }
                )

                message = EmailMultiAlternatives(
                    subject=f'Вот список новых Постов по категории "{cat}" за прошедшую неделю!',
                    from_email='pten4ik99@yandex.ru',
                    to=emails,
                )
                message.attach_alternative(html, 'text/html')
                message.send()
                print('Отправлено!')
