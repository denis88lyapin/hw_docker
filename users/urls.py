from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users.views import UserUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
