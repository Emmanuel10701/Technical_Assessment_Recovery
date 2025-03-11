from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthViewSet, ChatViewSet, UserDetailViewSet, TokenBalanceViewSet

# Initialize the router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'chat', ChatViewSet, basename='chat')
router.register(r'user-details', UserDetailViewSet, basename='user-details')
router.register(r'token-balance', TokenBalanceViewSet, basename='token-balance')

urlpatterns = [
    path('', include(router.urls)),
]
