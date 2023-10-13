from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from payment.models import Payment
from school.serializers import CourseSerializer, LessonSerializer
from users.models import User


class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    user = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'


class SuccessPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }
