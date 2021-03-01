import os

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .permissions import (IsAdminOrNone, IsAdminOrRead, IsAdminOrReadOnly,
                          IsModeratorAdminAuthor)
from .models import Category, Genre, Review, Title, PreUser
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          UserSerializer)
from .token import code_for_email

User = get_user_model()


class CreateListDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               GenericViewSet):
    pass


class GenresViewSet(CreateListDestroyViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('id')
    permission_classes = [IsAdminOrRead]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name', ]


class CategoryViewSet(CreateListDestroyViewSet):
    serializer_class = CategoriesSerializer
    queryset = Category.objects.all().order_by('id')
    permission_classes = [IsAdminOrRead]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleListSerializer
        return TitleCreateSerializer
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    filter_backends = (DjangoFilterBackend, SearchFilter)
    permission_classes = [IsAdminOrRead]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination


class UserInfo(APIView):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'PATCH'])
    def get(self, request):
        queryset = User.objects.get(username=request.user.username)
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrNone]
    queryset = User.objects.all()
    http_method_names = ('get', 'post', 'delete', 'patch', )
    lookup_field = 'username'


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsModeratorAdminAuthor | IsAdminOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id), id=review_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id), id=review_id
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly | IsModeratorAdminAuthor]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


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
