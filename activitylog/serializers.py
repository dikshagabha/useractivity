from rest_framework import serializers
from .models import UserActivityLog

class UserActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = ['id', 'user', 'action', 'timestamp', 'metadata', 'status']
        read_only_fields = ['id', 'timestamp', 'user']
