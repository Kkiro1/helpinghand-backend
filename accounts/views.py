from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user
    POST /api/auth/register/
    
    Body: {
        "username": "string",
        "email": "string",
        "password": "string",
        "password2": "string",
        "first_name": "string",
        "last_name": "string"
    }
    """
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user_serializer = UserSerializer(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': user_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login user and return JWT tokens
    POST /api/auth/login/
    
    Body: {
        "username": "string",
        "password": "string"
    }
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        validated_data = serializer.validated_data
        user = validated_data['user']
        
        user_serializer = UserSerializer(user)
        
        return Response({
            'message': 'Login successful',
            'user': user_serializer.data,
            'tokens': {
                'refresh': validated_data['refresh'],
                'access': validated_data['access']
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    Get current authenticated user profile
    GET /api/auth/me/
    
    Headers: {
        "Authorization": "Bearer <access_token>"
    }
    """
    serializer = UserSerializer(request.user)
    
    return Response({
        'user': serializer.data
    }, status=status.HTTP_200_OK)