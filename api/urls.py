from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitlesViewSet, UserInfo, UserViewSet)

router = DefaultRouter()
router.register('genres', GenresViewSet)
router.register('categories', CategoryViewSet)
router.register('titles', TitlesViewSet)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='Review'
)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='Comment'
)
router.register('users', UserViewSet, basename='useroperations')

urlpatterns = [

    path("users/me/", UserInfo.as_view()),
    path('', include(router.urls)),
]
