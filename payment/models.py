import uuid

from django.db import models

from config import settings
from school.models import Course, Lesson
from users.models import NULLABLE


class Payment(models.Model):
    METHOD_CASH = 'cash'
    METHOD_TRANSFER = 'transfer'

    PAID_METHOD = (
        (METHOD_CASH, 'наличными'),
        (METHOD_TRANSFER, 'перевод'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='оплачен курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name='оплачен урок')

    date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    method = models.CharField(max_length=20, choices=PAID_METHOD, verbose_name='способ оплаты:')

    # Stripe
    uid = models.UUIDField(default=uuid.uuid4, editable=False, **NULLABLE)
    stripe_id = models.CharField(max_length=255, unique=True, editable=False, **NULLABLE)
    status = models.CharField(max_length=10, **NULLABLE)
    customer_email = models.EmailField(**NULLABLE)


    def __str__(self):
        return f'{self.user} {self.course if self.course else self.lesson}, {self.payment_amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
