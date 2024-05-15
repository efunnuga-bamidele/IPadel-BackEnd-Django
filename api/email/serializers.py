# serializers.py

from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    to_email = serializers.EmailField()
    subject = serializers.CharField()
    message = serializers.CharField()
    displayName = serializers.CharField()
