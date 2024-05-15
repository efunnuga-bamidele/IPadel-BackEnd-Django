# # serializers.py

# from rest_framework import serializers
# from .models import PasswordResetToken


# class PasswordResetTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PasswordResetToken
#         fields = '__all__'
# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PasswordResetToken


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    new_password = serializers.CharField(required=False)
