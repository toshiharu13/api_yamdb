from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import GenresViewSet, UserInfo

router = DefaultRouter()
router.register('genres', GenresViewSet)
# router.register('titles', TitlesViewSet)

# router.register('posts', PostViewSet)
# router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')
# router.register('group', GroupViewSet)
# router.register('follow', FollowViewSet, basename='follows')


urlpatterns = [
    path('', include(router.urls)),
    path("users/me/", UserInfo.as_view()),
]
