from __future__ import annotations

import re
from typing import Tuple

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile

User = get_user_model()


def _split_full_name(full_name: str) -> Tuple[str, str]:
    full_name = (full_name or '').strip()
    if not full_name:
        return '', ''
    parts = [p for p in full_name.split(' ') if p]
    if len(parts) == 1:
        return parts[0], ''
    return parts[0], ' '.join(parts[1:])


def _slugify_username(raw: str) -> str:
    raw = (raw or '').strip().lower()
    raw = raw.split('@')[0]  # if user passed an email
    raw = re.sub(r'[^a-z0-9_\.]+', '_', raw)
    raw = re.sub(r'_+', '_', raw).strip('_')
    return raw or 'user'


def _unique_username(base: str) -> str:
    base = _slugify_username(base)
    candidate = base
    i = 1
    while User.objects.filter(username=candidate).exists():
        i += 1
        candidate = f"{base}{i}"
    return candidate


class RegisterSerializer(serializers.Serializer):
    """
    Accept BOTH:

    Frontend payload (current React):
      { fullName, email, password, role }

    Legacy payload (old API):
      { username, email, password, password2, first_name, last_name }
    """

    # Frontend fields
    fullName = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(
        choices=[c[0] for c in UserProfile.ROLE_CHOICES],
        required=False,
        allow_blank=True,
    )

    # Legacy fields
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    password2 = serializers.CharField(required=False, allow_blank=True, write_only=True)

    # Shared
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
    )

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password2 and password != password2:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # Determine name
        full_name = attrs.get('fullName')
        if full_name:
            first, last = _split_full_name(full_name)
        else:
            first = (attrs.get('first_name') or '').strip()
            last = (attrs.get('last_name') or '').strip()

        # Determine username
        username = (attrs.get('username') or '').strip()
        if not username:
            username = _unique_username(attrs.get('email', 'user'))
        else:
            username = _unique_username(username)

        # Determine role
        role = (attrs.get('role') or '').strip() or UserProfile.ROLE_DONOR

        attrs['first_name'] = first
        attrs['last_name'] = last
        attrs['username'] = username
        attrs['role'] = role
        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role', UserProfile.ROLE_DONOR)
        validated_data.pop('password2', None)
        validated_data.pop('fullName', None)

        password = validated_data.pop('password')

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(password)
        user.save()

        # Ensure profile exists & set role
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = role

        # Prefer fullName as display_name (esp. organization signup)
        full_name = (self.initial_data.get('fullName') or '').strip()
        if full_name:
            profile.display_name = full_name
        else:
            ui_name = (user.get_full_name() or '').strip()
            if ui_name:
                profile.display_name = ui_name

        profile.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Accept BOTH:

    Frontend payload:
      { email, password, userType }

    Legacy payload:
      { username, password }
    """

    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
    )
    userType = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        password = attrs.get('password')
        email = attrs.get('email')
        username = attrs.get('username')
        user_type = (attrs.get('userType') or '').strip()

        user = None
        if email:
            user = User.objects.filter(email__iexact=email).first()
            if not user:
                raise serializers.ValidationError('Invalid credentials. Please try again.')
            username = user.username

        if not username:
            raise serializers.ValidationError('username or email is required.')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials. Please try again.')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        # Optional role check
        if user_type:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            if profile.role == UserProfile.ROLE_BOTH:
                if user_type not in (UserProfile.ROLE_DONOR, UserProfile.ROLE_RECIPIENT, UserProfile.ROLE_BOTH):
                    raise serializers.ValidationError('Role mismatch.')
            elif profile.role != user_type:
                raise serializers.ValidationError('Role mismatch.')

        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username', 'first_name', 'last_name', 'role', 'date_joined')
        read_only_fields = ('id', 'date_joined')

    def get_role(self, obj) -> str:
        profile = getattr(obj, 'profile', None)
        return getattr(profile, 'role', UserProfile.ROLE_DONOR)

    def get_name(self, obj) -> str:
        profile = getattr(obj, 'profile', None)
        if profile and profile.display_name:
            return profile.display_name
        full = (obj.get_full_name() or '').strip()
        return full if full else obj.username
