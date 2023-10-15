from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from school.models import Course, Lesson, Subscription
from school.paginators import CourseAndLessonPaginator
from school.permissions import IsModeratorViewSet, IsOwnerOrSuperuser, IsModerator
from school.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from school.tasks import subscription_mailing


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser | IsModeratorViewSet]
    pagination_class = CourseAndLessonPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        subscription_mailing.delay(course.id, 'Course')
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        subscription_mailing.delay(lesson.id, 'Lesson')


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser | IsModerator]
    pagination_class = CourseAndLessonPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser | IsModerator]

    def update(self, request, *args, **kwargs):
        lesson = self.get_object()
        subscription_mailing.delay(lesson.id, 'Lesson')
        return super().update(request, *args, **kwargs)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser]
