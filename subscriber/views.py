from rest_framework import viewsets
from utils.notifiers import NotifierFactory

from subscriber.serializers import UserSerializer, ChannelSerializer, CategorySerializer, NotificationSerializer, \
    MessageSerializer
from django.contrib.auth import get_user_model
from .models import Channel, Category, Notification, Message
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all().order_by('-created')
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        user = get_user_model()
        username = self.request.data.get('username')
        email = self.request.data.get('email')
        queryset, _ = user.objects.get_or_create(username=username, email=email)
        queryset.first_name = self.request.data.get('first_name')
        queryset.last_name = self.request.data.get('last_name')
        queryset.phone_number = self.request.data.get('phone_number')
        queryset.subscribed.set(self.request.data.get('subscribed'))
        queryset.channels.set(self.request.data.get('channels'))
        queryset.save()
        serializer = UserSerializer(queryset)
        return Response(serializer.data)


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all().order_by('-created')
    serializer_class = ChannelSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-created')
    serializer_class = CategorySerializer


def notify_users(category_id, message):
    user = get_user_model()
    users = user.objects.all().filter(subscribed__in=category_id)
    factory = NotifierFactory()

    for user in users:
        for channel in user.channels.all():
            Notification.objects.create(user=user, channel=channel, message=message)
            notifier = factory.create(str(channel).upper())
            notifier.notify(user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created')
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        category_id = self.request.data.get('category')
        message = Message.objects.create(
            category=Category.objects.get(id=category_id), message=self.request.data.get('message'))
        serializer = MessageSerializer(message)

        notify_users(category_id, message)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all().order_by('-created')
    serializer_class = NotificationSerializer
