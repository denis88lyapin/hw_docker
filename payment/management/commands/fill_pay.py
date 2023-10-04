from django.core.management import BaseCommand
from payment.models import Payment
from school.models import Course, Lesson
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user1 = User.objects.filter(email='test1@test.ru').first()
        user2 = User.objects.filter(email='test2@test.ru').first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if user1 and course:
            payment = Payment.objects.create(
                user=user1,
                course=course,
                payment_amount=100000,
                method=Payment.METHOD_CASH
            )

        if user2 and lesson:
            payment1 = Payment.objects.create(
                user=user2,
                lesson=lesson,
                payment_amount=1000,
                method=Payment.METHOD_TRANSFER
            )
