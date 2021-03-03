from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api_yamdb import settings

from .filters import TitleFilter
from .mixins import ListPostDelMix
from .models import Category, Genre, PreUser, Review, Title
from .permissions import (IsAdminOrNone, IsAdminOrRead, IsAdminOrReadOnly,
                          IsModeratorAdminAuthor)
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenreSerializer, PreUserSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          UserSerializer)
from .token import code_for_email
from .utils import get_tokens_for_user

User = get_user_model()


class GenresViewSet(ListPostDelMix):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('id')
    permission_classes = [IsAdminOrRead]
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name', ]


class CategoryViewSet(ListPostDelMix):
    serializer_class = CategoriesSerializer
    queryset = Category.objects.all().order_by('id')
    permission_classes = [IsAdminOrRead]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    filter_backends = (DjangoFilterBackend, SearchFilter)
    permission_classes = [IsAdminOrRead]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleListSerializer
        return TitleCreateSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrNone]
    queryset = User.objects.all()
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated],)
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    serializer = PreUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(confirmation_code=code_to_send)
    send_mail(
        subject='Activate your account.',
        message=r'Activation code {code_to_send}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[serializer.validated_data.get('email')],
    )
    return Response(serializer.data)


@api_view(['POST'])
def token_send(request):
    """Если в временной БД есть такой пользователь + пароль
     берем/создаём пользователя"""
    serializer = PreUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email_to_check = serializer.validated_data.get('email')
    code_to_check = serializer.validated_data.get('confirmation_code')
    if PreUser.objects.filter(
            email=email_to_check,
            confirmation_code=code_to_check).exists():
        user_to_check, user_created = User.objects.get_or_create(
            email=email_to_check)
        token_to_send = get_tokens_for_user(user_to_check)
        return Response(token_to_send)
    else:
        return Response({'field_name': 'error, no such user'},
                        status=status.HTTP_400_BAD_REQUEST)
