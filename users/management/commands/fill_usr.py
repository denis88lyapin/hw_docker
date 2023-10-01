from django.core.management import BaseCommand
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='test@test.ru',
            first_name='test',
            last_name='test_',
            is_active=True
        )
        user.set_password('test')
        user.save()

        user1 = User.objects.create(
            email='test1@test.ru',
            first_name='test1',
            last_name='test1_',
            is_active=True
        )
        user1.set_password('test1')
        user1.save()