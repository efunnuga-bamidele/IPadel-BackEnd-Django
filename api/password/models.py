from django.db import models
from api.user.models import CustomUser


class PasswordResetToken(models.Model):
    # Use the custom user model
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
