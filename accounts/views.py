from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
import accounts.models as accounts_models
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
# Create your views here.


class UserView(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['get'])
    def get_user_list(self, request, *args, **kwargs):
        user_list = list(accounts_models.CustomUser.objects.filter(
            is_active=True).values('id', 'name', 'email'))
        return Response(data=user_list, status=status.HTTP_200_OK)


class AuthView(GenericViewSet):
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['post'])
    def register(self, request, *args, **kwargs):
        """
        Register a new user and return JWT tokens
        """
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name', '')
        mobile = request.data.get('mobile', '')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user already exists
        if accounts_models.CustomUser.objects.filter(email=email).exists():
            return Response(
                {'error': 'User with this email already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            return Response(
                {'error': 'Password validation failed', 'details': e.messages}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user
        try:
            user = accounts_models.CustomUser.objects.create_user(
                email=email,
                password=password,
                name=name,
                mobile=mobile
            )

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User registered successfully',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'mobile': user.mobile
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': 'Failed to create user', 'details': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        """
        Login user and return JWT tokens
        """
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user
        user = authenticate(email=email, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'User account is disabled'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'mobile': user.mobile
            }
        }, status=status.HTTP_200_OK)

