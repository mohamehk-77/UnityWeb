#!/usr/bin/python3

"""message application useing django"""

from django.db import models


class Message(models.Model):
    """Message model for storing messages in the database."""

    author = models.CharField("Author's name", max_length=100)
    email = models.EmailField("Author's Email", unique=True)
    subject = models.CharField("Subject", max_length=255)
    body = models.TextField("Body")
    sender = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class MessageRequest(models.Model):
    """Request for sending a new message, saved to the database."""

    sender = models.CharField(max_length=100)
    content = models.TextField()

    def send(self):
        """Save the request into the database and return its ID."""

        msg = Message(sender=self.sender, content=self.content)
        msg.save()
        return msg.id
