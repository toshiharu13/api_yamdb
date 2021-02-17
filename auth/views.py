from django.core.mail import EmailMessage
from django.shortcuts import render
from .token import code_for_email
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def mail_send(request, *args, **kwargs):
    to_email = request.args.get('email')
    mail_subject = 'Activate your account.'
    message = code_for_email()
    send_mail(
        mail_subject,
        message,
        'testproject@example.com',
        [to_email],
    )

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
