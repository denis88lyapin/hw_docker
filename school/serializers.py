from rest_framework import serializers

from school.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lesson_set.all.count')
    lessons = serializers.SerializerMethodField()

    # lessons_count = serializers.SerializerMethodField()

    # def get_lessons_count(self, instance):
    #     if instance.lesson_set.all():
    #         return instance.lesson_set.all().count()
    #     return 0

    def get_lessons(self, course):
        return LessonListSerializer(Lesson.objects.filter(course=course), many=True).data

    class Meta:
        model = Course
        fields = '__all__'
        # fields = ('id', 'course_name', 'course_preview', 'course_description', 'lessons_count')


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
