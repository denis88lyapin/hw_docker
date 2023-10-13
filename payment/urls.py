from django.urls import path

from payment.apps import PaymentConfig
from payment.views import PaymentListAPIView, PaymentCreateAPIView, PaymentSuccessView

app_name = PaymentConfig.name

urlpatterns = [
    path('list/', PaymentListAPIView.as_view(), name='payment_list'),
    path('create/', PaymentCreateAPIView.as_view(), name='create'),
    path('success/', PaymentSuccessView.as_view(), name='success')

]
