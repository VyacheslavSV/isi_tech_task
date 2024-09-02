from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError

from app_chat.models import Thread, Message


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'

    def validate(self, data):
        participants = data.get('participants')

        if participants and len(participants) != 2:
            raise DRFValidationError("A thread must have exactly 2 participants.")

        return data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'thread']
