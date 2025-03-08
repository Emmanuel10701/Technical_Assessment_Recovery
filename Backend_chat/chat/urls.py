from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthViewSet, ChatViewSet, TokenBalanceViewSet, UserDetailViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'chat', ChatViewSet, basename='chat')
router.register(r'tokens', TokenBalanceViewSet, basename='tokens')
router.register(r'user', UserDetailViewSet, basename='user-detail') 

urlpatterns = [
    path('', include(router.urls)),
]
