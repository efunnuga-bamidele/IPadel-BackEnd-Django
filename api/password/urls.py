
from django.urls import path
from .views import PasswordResetRequestView

urlpatterns = [
    path('password-reset/', PasswordResetRequestView.as_view(),
         name='password_reset'),
    path('password-reset/<str:token>/',
         PasswordResetRequestView.as_view(), name='password_reset_verify'),
]
