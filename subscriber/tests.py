from rest_framework import status
from rest_framework.test import APITestCase

from category.models import Category
from .models import Channel, User, Message


class ChannelTests(APITestCase):
    url = '/channel/'

    def test_create_channel(self):
        """
        Ensure we can create a new channel.
        """
        data = {'name': 'Email'}

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Channel.objects.count(), 1)
        self.assertEqual(Channel.objects.get().name, 'Email')

    def test_list_channels(self):
        """
        Ensure we can get channels list.
        """
        Channel.objects.create(name='Email')
        Channel.objects.create(name='SMS')
        Channel.objects.create(name='Push')

        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Channel.objects.count(), 3)
        self.assertEqual(Channel.objects.get(id=1).name, 'Email')
        self.assertEqual(Channel.objects.get(id=2).name, 'SMS')
        self.assertEqual(Channel.objects.get(id=3).name, 'Push')


class UserTests(APITestCase):
    url = '/users/'

    def setUp(self):
        create_base_categories_and_channels()

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        data = {
            "username": "username",
            "first_name": "first",
            "last_name": "last",
            "email": "email@example.com",
            "phone_number": "+1 123 456 7890",
            "subscribed": [],
            "channels": [],
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'username')

    def test_list_user(self):
        """
        Ensure we can get users list.
        """
        create_base_users()

        response = self.client.get(self.url, format='json')
        users = response.json().get('results')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(users[0].get('subscribed'), ['Sports', 'Finance', 'Movies'])
        self.assertEqual(users[1].get('subscribed'), ['Movies'])
        self.assertEqual(users[2].get('subscribed'), ['Finance'])
        self.assertEqual(users[3].get('subscribed'), ['Sports'])
        self.assertEqual(users[4].get('subscribed'), [])

        self.assertEqual(users[0].get('channels'), ['SMS', 'Push', 'Email'])
        self.assertEqual(users[1].get('channels'), ['SMS'])
        self.assertEqual(users[2].get('channels'), ['Push'])
        self.assertEqual(users[3].get('channels'), ['Email'])
        self.assertEqual(users[4].get('channels'), [])


class MessagesNotificationsTests(APITestCase):
    def setUp(self):
        create_base_categories_and_channels()
        create_base_users()

    def test_create_message(self):
        """
        Ensure we can create a new message object.
        """
        data = {
            "message": "message 1",
            "category": 1,
        }

        response = self.client.post('/message/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().message, 'message 1')

    def test_list_messages(self):
        """
        Ensure we can get messages list.
        """
        self.client.post('/message/', {"message": "message 1", "category": 1}, format='json')
        self.client.post('/message/', {"message": "message 2", "category": 3}, format='json')
        response = self.client.get('/message/', format='json')
        messages = response.json().get('results')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].get('message'), 'message 2')
        self.assertEqual(messages[1].get('message'), 'message 1')

    def test_list_notifications(self):
        """
        Ensure we can get notifications list.
        """
        self.client.post('/message/', {"message": "message 1", "category": 1}, format='json')
        self.client.post('/message/', {"message": "message 2", "category": 2}, format='json')
        self.client.post('/message/', {"message": "message 3", "category": 3}, format='json')
        notifications = []
        response = self.client.get('/notifications/', format='json')
        notifications.extend(response.json().get('results'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(notifications), 10)
        response = self.client.get('/notifications/?page=2', format='json')
        notifications.extend(response.json().get('results'))
        self.assertEqual(len(notifications), 12)

        self.assertEqual(notifications[0], notifications[0] | {'user': 'John5 Doe5', 'channel': 'Email', 'message': 'message 3'})
        self.assertEqual(notifications[1], notifications[1] | {'user': 'John5 Doe5', 'channel': 'Push', 'message': 'message 3'})
        self.assertEqual(notifications[2], notifications[2] | {'user': 'John5 Doe5', 'channel': 'SMS', 'message': 'message 3'})
        self.assertEqual(notifications[3], notifications[3] | {'user': 'John4 Doe4', 'channel': 'SMS', 'message': 'message 3'})
        self.assertEqual(notifications[4], notifications[4] | {'user': 'John5 Doe5', 'channel': 'Email', 'message': 'message 2'})
        self.assertEqual(notifications[5], notifications[5] | {'user': 'John5 Doe5', 'channel': 'Push', 'message': 'message 2'})
        self.assertEqual(notifications[6], notifications[6] | {'user': 'John5 Doe5', 'channel': 'SMS', 'message': 'message 2'})
        self.assertEqual(notifications[7], notifications[7] | {'user': 'John3 Doe3', 'channel': 'Push', 'message': 'message 2'})
        self.assertEqual(notifications[8], notifications[8] | {'user': 'John5 Doe5', 'channel': 'Email', 'message': 'message 1'})
        self.assertEqual(notifications[9], notifications[9] | {'user': 'John5 Doe5', 'channel': 'Push', 'message': 'message 1'})
        self.assertEqual(notifications[10], notifications[10] | {'user': 'John5 Doe5', 'channel': 'SMS', 'message': 'message 1'})
        self.assertEqual(notifications[11], notifications[11] | {'user': 'John2 Doe2', 'channel': 'Email', 'message': 'message 1'})


def create_user(username, first_name, last_name, email, subscribed, channels):
    user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
    for channel in channels:
        user.channels.add(channel)
    for category in subscribed:
        user.subscribed.add(category)


def create_base_users():
    create_user('user_1', 'John1', 'Doe1', 'email1@example.com', [], [])
    create_user('user_2', 'John2', 'Doe2', 'email2@example.com', [1], [3])
    create_user('user_3', 'John3', 'Doe3', 'email3@example.com', [2], [2])
    create_user('user_4', 'John4', 'Doe4', 'email4@example.com', [3], [1])
    create_user('user_5', 'John5', 'Doe5', 'email5@example.com', [1, 2, 3], [1, 2, 3])


def create_base_categories_and_channels():
    Category.objects.create(name='Sports')
    Category.objects.create(name='Finance')
    Category.objects.create(name='Movies')
    Channel.objects.create(name='SMS')
    Channel.objects.create(name='Push')
    Channel.objects.create(name='Email')
