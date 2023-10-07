from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from school.models import Course, Lesson, Subscription
from users.models import User


class LessonCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test3@test.ru')
        self.user.set_password('test3')
        self.user.save()

        self.token = AccessToken.for_user(self.user)
        # refresh = RefreshToken.for_user(self.user)
        # self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.course = Course.objects.create(
            course_name='Test',
            course_description='Test description',
            owner=self.user)

        self.lesson = Lesson.objects.create(
            lesson_name='TestLesson',
            lesson_description='Test lesson description',
            video_url='https://www.youtube.com/',
            course=self.course,
            owner=self.user
        )

    def test_lesson_create(self):
        url = reverse('school:lesson_create')
        data = {
            'lesson_name': 'TestLesson1',
            'lesson_description': 'Test lesson description1',
            'video_url': 'https://www.youtube.com/',
            "course": self.course.id,
            "owner": self.user.id
        }

        response = self.client.post(url, data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            Lesson.objects.all().exists(),
            {
                'id': 2,
                'lesson_name': 'TestLesson1',
                'lesson_description': 'Test lesson description1',
                'video_url': 'https://www.youtube.com',
                'owner': 1,
                'course': 1
            }
        )

    def test_lesson_list(self):
        url = reverse('school:lesson_list')

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json().get('results'),
            [
                {
                    "id": self.lesson.pk,
                    "lesson_name": self.lesson.lesson_name,
                    "lesson_description": self.lesson.lesson_description,
                    "video_url": self.lesson.video_url,
                    "lesson_preview": self.lesson.lesson_preview,
                    "owner": self.user.pk,
                    "course": self.course.pk
                }
            ]
        )

    def test_lesson_detail(self):
        url = reverse('school:lesson_detail', kwargs={'pk': self.lesson.pk})

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json(),
            {
                "id": self.lesson.pk,
                "lesson_name": self.lesson.lesson_name,
                "lesson_description": self.lesson.lesson_description,
                "video_url": self.lesson.video_url,
                "lesson_preview": self.lesson.lesson_preview,
                "owner": self.user.pk,
                "course": self.course.pk
            }
        )

    def test_lesson_update_PUT(self):
        url = reverse('school:lesson_update', kwargs={'pk': self.lesson.pk})

        data = {
            "lesson_name": self.lesson.lesson_name,
            "lesson_description": "test_update",
            "video_url": self.lesson.video_url,
            "owner": self.user.pk,
            "course": self.course.pk
        }

        response = self.client.put(url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json(),
            {
                "id": self.lesson.pk,
                "lesson_name": self.lesson.lesson_name,
                "lesson_description": "test_update",
                "video_url": self.lesson.video_url,
                "lesson_preview": self.lesson.lesson_preview,
                "owner": self.user.pk,
                "course": self.course.pk
            }
        )

    def test_lesson_update_PATCH(self):
        url = reverse('school:lesson_update', kwargs={'pk': self.lesson.pk})

        data = {
            "lesson_description": "test_update",
        }

        response = self.client.patch(url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json(),
            {
                "id": self.lesson.pk,
                "lesson_name": self.lesson.lesson_name,
                "lesson_description": "test_update",
                "video_url": self.lesson.video_url,
                "lesson_preview": self.lesson.lesson_preview,
                "owner": self.user.pk,
                "course": self.course.pk
            }
        )

    def test_lesson_delete(self):
        url = reverse('school:lesson_delete', kwargs={'pk': self.lesson.pk})

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Lesson.objects.all().exists(),
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test3@test.ru')
        self.user.set_password('test3')
        self.user.save()

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(
            course_name='Test',
            course_description='Test description',
            owner=self.user)

        self.subscription = Subscription.objects.create(course=self.course, user=self.user)

    def test_subscription_create(self):
        url = reverse('school:subscription')
        print(url)

        data = {
            'course': self.course.id,
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertEquals(
            response.json(),
            {
                'id': 2,
                "course": 1,
                "user": 1,
                "is_active": False
            }
        )

    def test_subscription_list(self):
        url = reverse('school:subscription')

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json(),
            [
                {
                    'id': self.subscription.pk,
                    "course": self.course.pk,
                    "user": self.user.pk,
                    "is_active": self.subscription.is_active
                }
            ]
        )

    def test_subscription_update(self):
        url = reverse('school:subscription', kwargs={'pk': self.subscription.pk})

        data = {
            "is_active": True,
        }

        response = self.client.patch(url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json(),
            {
                'id': self.subscription.pk,
                "course": self.course.pk,
                "user": self.user.pk,
                "is_active": True
            }
        )

    def test_subscription_retrieve(self):
        url = reverse('school:subscription', kwargs={'pk': self.subscription.pk})

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(
            response.json(),
            {
                'id': self.subscription.pk,
                "course": self.course.pk,
                "user": self.user.pk,
                "is_active": self.subscription.is_active
            }
        )

    def test_subscription_delete(self):
        url = reverse('school:subscription', kwargs={'pk': self.subscription.pk})

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Subscription.objects.all().exists(),
        )
