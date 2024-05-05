#!/usr/bin/python3

"""message application useing django"""

from django.contrib import admin
from .models import Message, MessageRequest

admin.site.register(Message)
admin.site.register(MessageRequest)
