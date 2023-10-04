from django.db import models

from config import settings
from users.models import NULLABLE


class Course(models.Model):
    course_name = models.CharField(max_length=250, verbose_name='наименование')
    course_preview = models.ImageField(upload_to='school/course/', verbose_name='превью', **NULLABLE)
    course_description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    def __str__(self):
        return f'{self.course_name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=250, verbose_name='наименование')
    lesson_description = models.TextField(verbose_name='описание')
    lesson_preview = models.ImageField(upload_to='school/lesson/', verbose_name='превью', **NULLABLE)
    video_url = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')

    def __str__(self):
        return f'{self.lesson_name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
