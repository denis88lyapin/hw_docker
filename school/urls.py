from django.urls import path

from school.apps import SchoolConfig
from rest_framework.routers import DefaultRouter

from school.views import (CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView,
                          LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionViewSet)

app_name = SchoolConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'subscription', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/detail/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
] + router.urls
