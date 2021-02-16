from django.urls import path, include
#from rest_framework_simplejwt.views import (TokenObtainPairView)
from .views import MailSend, TokenSend

urlpatterns = [
    path('email/', MailSend),
    path('token/', TokenSend),
]