from category.models import Category
from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['created']


class Channel(BaseModel):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True, blank=True)
    subscribed = models.ManyToManyField(Category)
    channels = models.ManyToManyField(Channel)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Message(BaseModel):
    message = models.TextField(max_length=200, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.message


class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
