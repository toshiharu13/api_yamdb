from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitlesViewSet, UserViewSet, mail_send,
                    token_send)

router_v1 = DefaultRouter()
router_v1.register('genres', GenresViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('titles', TitlesViewSet)
router_v1.register(r'titles/(?P<title_id>[0-9]+)/reviews',
                   ReviewViewSet,
                   basename='Review'
                   )
router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='Comment'
)
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/email/', mail_send),
    path('v1/auth/token/', token_send),
    path('v1/', include(router_v1.urls)),
]
