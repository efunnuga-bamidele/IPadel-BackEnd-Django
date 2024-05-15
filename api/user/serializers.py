from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes, permission_classes

from .models import CustomUser


# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=True, required=False)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id', 'displayName', 'email', 'password', 'avatar', 'isVerified', 'phoneNumber', 'referralCode', 'isBlacklisted', 'gender', 'country',
                  'state', 'city', 'expartiseLevel', 'accessLevel', 'session_token', 'created_at', 'updated_at', 'is_active', 'referredBy', 'agreeToTerms', 'first_name', 'last_name')
