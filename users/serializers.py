from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import UserProfile

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.IntegerField(required=False, default=0)

    class Meta:
        fields = ['email', 'password', 'remember_me']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({_('password'): _('Passwords must match')})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
        )
        user.save()
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'profile_picture']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        if new_password != confirm_password:
            raise serializers.ValidationError({
                _('confirm_password'): _('New password and confirm password do not match.')
            })
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError({
                _('old_password'): _('Old password is incorrect.')
            })
        try:
            validate_password(new_password, user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({
                _('new_password'): e.messages
            })

        return attrs



