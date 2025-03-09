from django.urls import path, include
from .views import UserViewSet, AuthViewSet, ChatViewSet, TokenBalanceViewSet, UserDetailViewSet
urlpatterns = [
    path('users/create/', UserViewSet.as_view({'post': 'create'}), name='user-create'),
    path('auth/login/', AuthViewSet.as_view({'post': 'login'}), name='auth-login'),
    path('chat/send_message/', ChatViewSet.as_view({'post': 'send_message'}), name='chat-send'),
    path('tokens/balance/', TokenBalanceViewSet.as_view({'get': 'balance'}), name='tokens-balance'),
    path('user/details/', UserDetailViewSet.as_view({'get': 'details'}), name='user-details'),
]