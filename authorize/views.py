import os

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PreUser
from .token import code_for_email

User = get_user_model()


@api_view(['POST'])
def mail_send(request):
    code_to_send = code_for_email()
    to_email = request.data
    to_email = to_email.get('email')
    test_object = PreUser.objects.filter(email=to_email)
    if test_object:
        exist_pair = PreUser.objects.get(email=to_email)
        exist_pair.confirmation_code = code_to_send
    else:

        PreUser.objects.create(email=to_email, confirmation_code=code_to_send)

    mail_subject = 'Activate your account.'
    message = code_to_send
    admin_from = os.getenv('LOGIN')
    send_mail(
        mail_subject,
        message,
        admin_from,
        [to_email],
    )
    return Response({'email': to_email})


@api_view(['POST'])
def TokenSend(request):
    need_params = request.data
    email_to_check = need_params.get('email')
    code_to_check = need_params.get('confirmation_code')
    test_object = User.objects.filter(email=email_to_check)
    # если в БД есть такой пользователь сверяем пароль
    if test_object:
        object_user = User.objects.get(email=email_to_check)
        # если пароль совпадает генерируем токен
        if object_user.password == code_to_check:
            token_to_send = get_tokens_for_user(object_user)
            return Response(token_to_send)
        else:
            # ошибка если пара не совпадает
            return Response({'field_name': 'ERR'},
                            status=status.HTTP_400_BAD_REQUEST)
    #  если пользователя нет проверяем временную таблицу
    test_object = PreUser.objects.filter(email=email_to_check)
    if test_object:
        object_pre_u = PreUser.objects.get(email=email_to_check)
        if object_pre_u.confirmation_code == code_to_check:
            User.objects.create(email=email_to_check, password=code_to_check)
            token_to_send = get_tokens_for_user(object_pre_u)
            return Response(token_to_send)
    return Response({'field_name': 'ERR'},
                    status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'token': str(refresh.access_token),
    }
