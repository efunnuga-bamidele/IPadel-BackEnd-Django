from rest_framework import serializers
from .models import Court


# class CourtSerializer(serializers.HyperlinkedModelSerializer):
class CourtSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=True, required=False)

    class Meta:
        model = Court
        fields = '__all__'
