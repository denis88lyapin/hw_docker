from pprint import pprint
import stripe
from rest_framework.generics import get_object_or_404
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from config import settings
from payment.models import Payment
from payment.serializers import PaymentSerializer, SuccessPaymentSerializer
from payment.services import stripe_price_data
from school.models import Course, Lesson

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('course', 'lesson', 'user', 'method')
    ordering_fields = ('date',)

    def get_queryset(self):
        return Payment.objects.all(user=self.request.user.pk)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data

        if data.get('course'):
            product = get_object_or_404(Course, pk=data['course'])
        else:
            product = get_object_or_404(Course, pk=data['lesson'])
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': stripe_price_data(product),
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='http://localhost:8000/' +
                            reverse('payment:success') + '?session_id={CHECKOUT_SESSION_ID}')
            pprint(checkout_session.stripe_id)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(product, Course):
            pay = Payment.objects.create(
                user=self.request.user,
                course=product,
                payment_amount=data['payment_amount'],
                method=Payment.METHOD_TRANSFER,
                stripe_id=checkout_session.stripe_id,
                status=checkout_session['status'])
            pay.save()
        if isinstance(product, Lesson):
            pay = Payment.objects.create(
                user=self.request.user,
                lesson=product,
                payment_amount=data['payment_amount'],
                method=Payment.METHOD_TRANSFER,
                stripe_id=checkout_session.stripe_id,
                status=checkout_session['status'])
            pay.save()

        return Response({'payment_url': checkout_session.url}, status=status.HTTP_201_CREATED)


class PaymentSuccessView(generics.ListAPIView):
    serializer_class = SuccessPaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        session_id = self.request.GET.get('session_id')  # Получаем параметр session_id из URL
        if session_id:
            try:
                pay = Payment.objects.get(stripe_id=session_id)
                session = stripe.checkout.Session.retrieve(pay.stripe_id)
                pay.customer_email = session['customer_details']['email']
                pay.status = session['status']
                pay.save()
                return super().get(request, *args, **kwargs)
            except Payment.DoesNotExist:
                return Response({'error': 'Платеж не найден'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'session_id не передан в URL'}, status=status.HTTP_400_BAD_REQUEST)

# class PaymentCreateAPIView(generics.CreateAPIView):
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all()
#
#     def create(self, request, *args, **kwargs):
#         data = request.data
#
#         if data['course']:
#             product = get_object_or_404(Course, pk=data['course'])
#         else:
#             product = get_object_or_404(Course, pk=data['lesson'])
#         # print(product)
#
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': stripe_price_data(product),
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#
#             # success_url='http://127.0.0.1:8000/' + reverse('payment:success') + '?session_id={CHECKOUT_SESSION_ID}'
#
#             success_url=self.request.build_absolute_uri(
#                 reverse('payment:success'), kwargs={'?session_id': '{CHECKOUT_SESSION_ID}'}),
#             # success_url=self.request.build_absolute_uri(
#             #     reverse('payment:success', kwargs={'session_id': '{CHECKOUT_SESSION_ID}'})),
#             # cancel_url=self.request.build_absolute_uri('cancel')
#         )
#
#         pay = Payment.objects.create(
#             user=self.request.user,
#             course=product,
#             payment_amount=self.request.data['payment_amount'],
#             method=Payment.METHOD_TRANSFER,
#             stripe_id=checkout_session.stripe_id,
#             status=checkout_session['status'],
#         )
#
#         pprint(checkout_session.id)
#         pprint(pay.stripe_id)
#         pay.save()
#         return Response({'payment_url': checkout_session.url}, status=status.HTTP_201_CREATED)
#
#
# class PaymentSuccessView(generics.RetrieveAPIView):
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         session_id = request.GET.get('session_id')
#         # pprint(request.GET.get('session_id'))
#         # pay = get_object_or_404(Payment, stripe_id=request.GET.get('session_id'))
#
#         pprint(session_id)
#         pay = Payment.objects.get(stripe_id=session_id)
#         # pprint(pay)
#
#         # pay = get_object_or_404(Payment, stripe_id=request.GET.get('session_id'))
#
#         session = stripe.checkout.Session.retrieve(pay.stripe_id)
#
#         pay.customer_email = session['customer_details']['email']
#         pay.status = session['status']
#         pay.save()
#         return super().get(request, *args, **kwargs)
