from django.utils import timezone
from celery import shared_task
import logging
from users.models import User

logger = logging.getLogger(__name__)


@shared_task(name="user_ban")
def user_ban():
    logger.info("Начало задачи блокировки пользователей")
    date_delta = timezone.now() - timezone.timedelta(days=30)
    logger.info(f'Дата отсечки: {date_delta}')

    users = User.objects.filter(last_login__lt=date_delta)

    for user in users:
        if user.is_active:
            logger.info(f'Пользователь: {user}, последний вход: {user.last_login}')
            user.is_active = False
            user.save()
            logger.info(f'Пользователь: {user} заблокирован')

    logger.info("Завершение задачи блокировки пользователей")
