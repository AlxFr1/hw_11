from celery import shared_task
from celery import Celery

from django.core.mail import send_mail as django_send_mail

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@shared_task
def celery_send_mail(message, receiver):
    django_send_mail(
        subject='Reminder',
        message=f'{message}',
        from_email="noreply@mysite.com",
        recipient_list=[receiver],
    )
