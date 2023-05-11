from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.

#Sending mail

send_mail('This is the subject', 'this is the message', 'proximaagents@gmail.com', ['recepientemail@gmail.com'] )