from django.db import models

from config import settings
from users.models import NULLABLE


class Payment(models.Model):
    COURSE_PAID = 'course'
    LESSON_PAID = 'lesson'

    PAID = (
        (COURSE_PAID, 'Оплачен курс'),
        (LESSON_PAID, 'Оплачен урок'),
    )

    METHOD_CASH = 'cash'
    METHOD_TRANSFER = 'transfer'

    PAID_METHOD = (
        (METHOD_CASH, 'наличными'),
        (METHOD_TRANSFER, 'перевод'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    obj_paid = models.CharField(max_length=20, choices=PAID, **NULLABLE, verbose_name='оплачен курс или урок')
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    method = models.CharField(max_length=20, choices=PAID_METHOD, verbose_name='способ оплаты:')
