from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from payment.models import Payment
from school.serializers import CourseSerializer, LessonListSerializer
from users.models import User


class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonListSerializer(read_only=True)
    user = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'
