from rest_framework import routers
from django.urls import path, include
from . import views
from .views import ResendVerificationEmailView

router = routers.DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    path('login/', views.signin, name='signin'),
    path('logout/<int:id>/', views.signout, name='signout'),
    path('verify-email/<int:user_id>/',
         views.VerifyEmailView.as_view(), name='verify_email'),
    path('resend-verification-email/', ResendVerificationEmailView.as_view(),
         name='resend_verification_email'),
    path('', include(router.urls)),

]
