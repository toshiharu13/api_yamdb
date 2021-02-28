from django.urls import path

from .views import TokenSend, mail_send

urlpatterns = [
    path('email/', mail_send),
    path('token/', TokenSend),
]
