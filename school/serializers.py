from rest_framework import serializers

from school.models import Course, Lesson, Subscription
from school.validators import URL_Validator


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(read_only=True, source='lesson_set.count')
    lessons = serializers.SerializerMethodField(read_only=True)
    subscription = serializers.SerializerMethodField(read_only=True)

    # lessons_count = serializers.SerializerMethodField()

    # def get_lessons_count(self, instance):
    #     if instance.lesson_set.all():
    #         return instance.lesson_set.all().count()
    #     return 0

    def get_lessons(self, course):
        return LessonSerializer(Lesson.objects.filter(course=course), many=True).data

    def get_subscription(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = '__all__'
        # fields = ('id', 'course_name', 'course_preview', 'course_description', 'lessons_count')
        extra_kwargs = {
            'owner': {'required': False}
        }


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        extra_kwargs = {
            'owner': {'required': False}
        }
        validators = [URL_Validator(field='video_url')]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }
