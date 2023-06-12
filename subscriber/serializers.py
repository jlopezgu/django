from rest_framework import serializers
from .models import User, Channel, Notification, Message

COMMON_FIELDS = ['id', 'created', 'deleted']


class UserSerializer(serializers.ModelSerializer):
    subscribed = serializers.StringRelatedField(many=True)
    channels = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'subscribed', 'channels',
                  'created', 'deleted']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    channel = serializers.StringRelatedField()
    message = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = '__all__'
