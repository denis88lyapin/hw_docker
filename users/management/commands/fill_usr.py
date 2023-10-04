from django.core.management import BaseCommand
from users.models import User
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='test@test.ru',
            first_name='test',
            last_name='test_',
            is_staff=True,
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

        user2 = User.objects.create(
            email='test2@test.ru',
            first_name='test2',
            last_name='test2_',
            is_active=True
        )
        user2.set_password('test2')
        user2.save()

        moderators = Group.objects.create(name='moderators')
        change_permission_course = Permission.objects.get(codename='change_course')
        view_permission_course = Permission.objects.get(codename='view_course')
        change_permission_lesson = Permission.objects.get(codename='change_lesson')
        view_permission_lesson = Permission.objects.get(codename='view_lesson')

        moderators.permissions.add(
            change_permission_course,
            view_permission_course,
            change_permission_lesson,
            view_permission_lesson
        )

        moderators.user_set.add(user)
