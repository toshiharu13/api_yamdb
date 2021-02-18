from django.urls import path, include
#from rest_framework_simplejwt.views import (TokenObtainPairView)
from .views import mail_send, TokenSend

urlpatterns = [
    path('email/', mail_send),
    path('token/', TokenSend),
]