from rest_framework import serializers

from school.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lesson_set.all.count')

    # lessons_count = serializers.SerializerMethodField()

    # def get_lessons_count(self, instance):
    #     if instance.lesson_set.all():
    #         return instance.lesson_set.all().count()
    #     return 0

    class Meta:
        model = Course
        # fields = '__all__'
        fields = ('id', 'course_name', 'course_preview', 'course_description', 'lessons_count')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
