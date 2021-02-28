from django.urls import include, path

#from rest_framework_simplejwt.views import (TokenObtainPairView)
from .views import TokenSend, mail_send

urlpatterns = [
    path('email/', mail_send),
    path('token/', TokenSend),
]