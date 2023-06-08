from django.contrib import admin
from .models import User, Category, Message, Channel

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Message)
admin.site.register(Channel)
