from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import Chat
from .serializers import UserSerializer, ChatSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=400)

        user = User.objects.create(
            username=username,
            password=make_password(password),
            tokens=4000  # Initial token balance
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'message': 'User registered successfully'})

class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)

class ChatViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        user = request.user
        message = request.data.get('message')

        if not message:
            return Response({'error': 'Message is required'}, status=400)

        if user.tokens < 100:
            return Response({'error': 'Insufficient tokens'}, status=400)

        # Generate AI response (replace with actual AI integration)
        response = f"This is a dummy AI response for you accessing the chat as {user.username}."

        # Deduct 100 tokens only after generating response
        user.tokens -= 100
        user.save()
        # Store the chat
        chat = Chat.objects.create(user=user, message=message, response=response)
        return Response({'message': message, 'response': response, 'remaining_tokens': user.tokens})
class UserDetailViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def details(self, request):
        return Response({
            "username": request.user.username,
            "tokens": request.user.tokens,
        })

class TokenBalanceViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def balance(self, request):
        return Response({'tokens': request.user.tokens})
