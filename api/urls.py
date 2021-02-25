from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import GenresViewSet, CategoryViewSet

router = DefaultRouter()
router.register('genres', GenresViewSet)
router.register('categories', CategoryViewSet)
#router.register('titles', TitlesViewSet)

# router.register('titles', TitlesViewSet)

# router.register('posts', PostViewSet)
# router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')
# router.register('group', GroupViewSet)
# router.register('follow', FollowViewSet, basename='follows')


urlpatterns = [
    path('genres/<slug:slug>/', GenresViewSet, name="genres_slug"),
    path('', include(router.urls)),
]
