from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your models here.

secret_key = getattr(settings, 'MY_SECRET_KEY', settings.SECRET_KEY)
admin_email = getattr(settings, 'MY_ADMIN_EMAIL_ADDRESS',
                      settings.ADMIN_EMAIL_ADDRESS)


class CustomUser(AbstractUser):
    backend = 'django.contrib.auth.backends.ModelBackend'
    displayName = models.CharField(max_length=250, unique=True)
    email = models.EmailField(max_length=250, unique=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    avatar = models.CharField(max_length=2000, blank=True, null=True)
    isVerified = models.BooleanField(default=False)
    agreeToTerms = models.BooleanField(default=False)
    phoneNumber = models.CharField(max_length=20, blank=True, null=True)
    referralCode = models.CharField(max_length=20, blank=True, null=True)
    referredBy = models.CharField(max_length=20, blank=True, null=True)
    isBlacklisted = models.BooleanField(default=False)
    gender = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    expartiseLevel = models.CharField(
        max_length=100, blank=True, null=True, default='Amateur')
    session_token = models.CharField(max_length=10, default=0)
    accessLevel = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True)
    verification_token_created_at = models.DateTimeField(null=True, blank=True)

    # def __str__(self):
    #     return self.email

    def generate_verification_token(self):
        serializer = URLSafeTimedSerializer(
            secret_key)  # Replace with your secret key
        token = serializer.dumps(self.email)
        self.verification_token = token
        self.verification_token_created_at = timezone.now()
        self.save()

    def is_verification_token_valid(self):
        if self.verification_token_created_at:
            serializer = URLSafeTimedSerializer(secret_key)
            try:
                # 259200 seconds = 3 days
                serializer.loads(self.verification_token, max_age=259200)
                return True
            except:
                return False
        return False

    def resend_verification_email(self):
        if not self.isVerified or not self.is_verification_token_valid():
            self.generate_verification_token()
            self.save()
