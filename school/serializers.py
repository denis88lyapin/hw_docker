from rest_framework import serializers

from school.models import Course, Lesson
from school.validators import URL_Validator


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(read_only=True, source='lesson_set.count')
    lessons = serializers.SerializerMethodField()

    # lessons_count = serializers.SerializerMethodField()

    # def get_lessons_count(self, instance):
    #     if instance.lesson_set.all():
    #         return instance.lesson_set.all().count()
    #     return 0

    def get_lessons(self, course):
        return LessonSerializer(Lesson.objects.filter(course=course), many=True).data

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
