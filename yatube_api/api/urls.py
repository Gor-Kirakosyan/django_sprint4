from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FollowView

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments', 
    CommentViewSet, 
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/follow/', FollowView.as_view()),
]