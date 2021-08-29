import json
import os
from datetime import timedelta, datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore

from NewsPaper.models import Post


def mail_sender():
    if os.path.exists('subscribers.json'):
        with open('subscribers.json', 'r', encoding='utf8') as f:
            info = json.load(f)
        post_list = Post.objects.filter(datetime__range=[datetime.now() - timedelta(days=7), datetime.now()])

        for cat, emails in info.items():

            html = render_to_string(
                'NewsPaper/sender_mail.html',
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


class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            func=mail_sender,
            trigger=CronTrigger(week='*/1'),
            id='mail_sender',
            max_instances=1,
            replace_existing=True,
        )

        try:
            print('Задачник запущен')
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            print('Задачник остановлен')