from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Chat
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'tokens']

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'user', 'message', 'response', 'timestamp']
        read_only_fields = ['user', 'response', 'timestamp']
