from django.core.mail import EmailMessage
from django.shortcuts import render
from.token import account_activation_token

def MailSend(request, *args, **kwargs):
    to_email = kwargs.get('email')
    mail_subject = 'Activate your account.'
    message = account_activation_token.make_token()
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    pass

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
