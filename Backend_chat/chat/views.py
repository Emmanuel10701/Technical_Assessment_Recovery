import os
import numpy as np
import pandas as pd
import tensorflow as tf
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from .models import Chat
from .serializers import UserSerializer

User = get_user_model()

# --- LOAD AND TRAIN MODEL ---
# Define file paths
csv_path = os.path.join(os.path.dirname(__file__), "training_data.csv")
model_path = os.path.join(os.path.dirname(__file__), "simple_greeting_model.h5")

# Load dataset
df = pd.read_csv(csv_path, encoding="utf-8", on_bad_lines="skip")

# Handle missing values
df = df.dropna()

# Convert text to numerical features using TF-IDF
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(df["pattern"]).toarray()

# Encode intent labels
label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(df["intent"])

# Define a simple neural network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation="relu", input_shape=(X_tfidf.shape[1],)),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(len(label_encoder.classes_), activation="softmax")
])

# Compile the model
model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the model
model.fit(X_tfidf, y_train, epochs=50, verbose=1)

# Save the model
model.save(model_path)

# --- FUNCTION FOR PREDICTION ---
def predict_intent(message):
    """Predict the intent of a given user message."""
    message_tfidf = vectorizer.transform([message]).toarray()
    prediction = model.predict(message_tfidf)
    predicted_intent_index = np.argmax(prediction)
    predicted_intent = label_encoder.inverse_transform([predicted_intent_index])[0]

    return predicted_intent

# --- DJANGO API VIEWS ---
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

        # Predict intent using the trained ML model
        predicted_intent = predict_intent(message)

        # Generate a response based on intent
        response_text = f"Predicted intent: {predicted_intent}"  # Modify this to return better responses

        # Deduct tokens
        user.tokens -= 100
        user.save()

        # Store chat in database
        chat = Chat.objects.create(user=user, message=message, response=response_text)

        return Response({
            'message': message,
            'response': response_text,
            'predicted_intent': predicted_intent,
            'remaining_tokens': user.tokens
        })

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
