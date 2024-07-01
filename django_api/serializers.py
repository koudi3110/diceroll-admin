from rest_framework import serializers
from django_api.models import Settings

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Settings
        fields='__all__'