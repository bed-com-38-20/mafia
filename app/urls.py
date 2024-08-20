from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView
from rest_framework.routers import DefaultRouter
from .views import home, user_login, user_registration, DeleteAccountView, token, create_post, ChatRoomViewSet, MessageViewSet, search_user,PostListView,CreatePostView
from . import consumers
from django.conf.urls.static import static
from django.conf import settings


# REST API Router
router = DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet)


# URL patterns
urlpatterns = [
    path('home/', home, name='home'),
    path('posts/', PostListView.as_view(), name='post-list'),
   path('create_post/', CreatePostView.as_view(), name='create-post'),
    path('search_user/', search_user, name='search_user'),
    path('user_registration/', user_registration, name='user_registration'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('user_login/', user_login, name='user_login'),
    path('auth/token/', token, name='token'),
    path('create_post/', create_post, name='createpost'),
    path('api/delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
    path('chatrooms/<int:chatroom_pk>/messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'})),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
