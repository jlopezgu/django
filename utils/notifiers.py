import logging
from subscriber.models import User


class EmailNotifier:
    def notify(self, user: User):
        logging.debug(f'Email Notification for user {user.first_name} {user.last_name}')


class SMSNotifier:
    def notify(self, user: User):
        logging.debug(f'SMS Notification for user {user.first_name} {user.last_name}')


class PushNotifier:
    def notify(self, user: User):
        logging.debug(f'Push Notification for user {user.first_name} {user.last_name}')


class NotifierFactory:
    def __init__(self):
        self._builders = {}
        self.register_builder('EMAIL', EmailNotifier)
        self.register_builder('PUSH', PushNotifier)
        self.register_builder('SMS', SMSNotifier)

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)