from django.db import models

from config import settings
from users.models import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=250, verbose_name='наименование')
    preview = models.ImageField(upload_to='school/course/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')
    price = models.PositiveIntegerField(default=0, verbose_name='стоимость')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=250, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='school/lesson/', verbose_name='превью', **NULLABLE)
    video_url = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')
    price = models.PositiveIntegerField(default=0, verbose_name='стоимость')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='подписка')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    is_active = models.BooleanField(default=False, verbose_name='статус подписки')
