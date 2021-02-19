import os

from .models import PreUser
from django.shortcuts import render
from .token import code_for_email
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def mail_send(request):
    to_email = request.query_params
    to_email = to_email.get('email')
    test_object = PreUser.objects.filter(email=to_email)
    if test_object:
        exist_pair = PreUser.objects.get(email=to_email)
        code_to_send = exist_pair.confirmation_code
    else:
        code_to_send = code_for_email()
        PreUser.objects.create(email=to_email, confirmation_code=code_to_send)

    mail_subject = 'Activate your account.'
    message = code_to_send
    send_mail(
        mail_subject,
        message,
        'testproject@example.com',
        [to_email],
    )
    return Response({'email': to_email})

def TokenSend(request):
    pass

'''def create(self, request, *args, **kwargs):
    Follow.objects.get_or_create(
        following=get_object_or_404(User, username=kwargs.get('following')),
        user=self.request.user,
    )
    queryset = Follow.objects.filter(following=kwargs.get('following'), user=request.user)
    serializer = CommentSerializer(data=queryset)
    return Response(serializer.data, status=status.HTTP_201_CREATED)'''
