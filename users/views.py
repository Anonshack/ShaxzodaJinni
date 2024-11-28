from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from .models import UserProfile
from .serializers import (
    RegisterSerializer, LoginSerializer, UserListSerializer,
    UserProfileSerializer, ChangePasswordSerializer
)
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterAPIView(APIView):
    """
    User registration endpoint.
    """

    @swagger_auto_schema(
        operation_description="Register a new user.",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response("User created successfully"),
            400: "Bad Request"
        },
        tags=["User Registration"]
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    User login endpoint.
    """

    @swagger_auto_schema(
        operation_description="Log in a user and get tokens.",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response("Tokens returned successfully"),
            401: "Invalid credentials",
            400: "Bad Request"
        },
        tags=["User Login"]
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            remember_me = serializer.validated_data.get('remember_me', 0)

            user = authenticate(email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                if remember_me:
                    refresh.set_exp(lifetime=timedelta(days=30))
                return Response({
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh)
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    """
    List all users.
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of all users.",
        responses={200: UserListSerializer(many=True)},
        tags=["User Management"]
    )
    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        user_count = users.count()
        return Response({
            'user_count': user_count,
            'users': serializer.data
        })


class UserCountView(APIView):
    """
    Retrieve total user count.
    """

    @swagger_auto_schema(
        operation_description="Retrieve total user count.",
        responses={200: openapi.Response("Count returned successfully")},
        tags=["User Management"]
    )
    def get(self, request, *args, **kwargs):
        user_count = User.objects.count()
        return Response({'user_count': user_count}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """
    User profile management.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve logged-in user's profile information.",
        responses={200: UserProfileSerializer()},
        tags=["User Profile"]
    )
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            profile_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.profile.phone_number if hasattr(user, 'profile') else None,
                'email': user.email,
                'profile_picture': user.profile.profile_picture.url if hasattr(user, 'profile') and user.profile.profile_picture else None,
            }
            return Response(profile_data, status=status.HTTP_200_OK)
        return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_description="Update logged-in user's profile.",
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer()},
        tags=["User Profile"]
    )
    def put(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete logged-in user's profile picture.",
        responses={200: "Profile picture deleted successfully."},
        tags=["User Profile"]
    )
    def delete(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if profile.profile_picture:
            profile.profile_picture.delete()
            profile.save()
            return Response({"message": "Profile picture deleted successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Profile picture not found."}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    User logout endpoint.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Log out a user by blacklisting their refresh token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token to blacklist')
            }
        ),
        responses={200: "Logout successful.", 400: "Bad Request"},
        tags=["User Logout"]
    )
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "refresh_token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    User password change endpoint.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Change the logged-in user's password.",
        request_body=ChangePasswordSerializer,
        responses={200: "Password changed successfully!", 400: "Bad Request"},
        tags=["User Profile"]
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
