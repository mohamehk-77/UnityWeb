#!/usr/bin/python3

"""message application useing django"""

from django.shortcuts import render
from django.http import HttpResponse
from .models import Message, MessageRequest


def view_messages(request):
    messages = Message.objects.all()
    return render(request, "messages.html", {'messages': messages})


def send_messages(request):
    if request.method == 'POST':  # If the form has been submitted...
        message = MessageRequest(name=request.POST['name'], email=request.POST['email'],
                                 subject=request.POST['subject'],
                                 body=request.POST['body'])
        message.save()  # Save the data to the database
        return HttpResponse('<p>Thank you for your message!</p><p><a href="/">Back</a></p>')
    else:  # This is a normal GET request, so give them the form to fill in
        return render(request, 'send_message.html', {})
