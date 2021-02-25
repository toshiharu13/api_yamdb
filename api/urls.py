from django.urls import path, include

from rest_framework.routers import DefaultRouter


from .views import GenresViewSet, UserInfo, UserViewSet, CategoryViewSet


router = DefaultRouter()
router.register('genres', GenresViewSet)
router.register('categories', CategoryViewSet)
#router.register('titles', TitlesViewSet)

# router.register('titles', TitlesViewSet)

# router.register('posts', PostViewSet)
# router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')
# router.register('group', GroupViewSet)
# router.register('follow', FollowViewSet, basename='follows')
router.register('users', UserViewSet, basename='useroperations')



urlpatterns = [

    path("users/me/", UserInfo.as_view()),
    path('', include(router.urls)),
]
