from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from django.contrib.auth import get_user_model
from authentication.models import Tokens, Otp
import secrets
from django.contrib.auth import authenticate


def generate_secure_otp():
    """
    Generate a secure random 6-digit OTP.

    Returns:
    - str: The generated 6-digit OTP.
    """
    # Generate a random integer with 6 digits
    otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))

    return otp


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return get_user_model().objects.create(**validated_data)


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tokens
        fields = ['token']

    def validate(self, attrs):
        """validate the token and activate the account"""
        token = attrs.get('token', None)

        if not token:
            raise serializers.ValidationError(
                {"token": "No token received"},
                code=400
            )

        if not Tokens.objects.filter(token=token, is_valid=True).exists():
            raise serializers.ValidationError(
                {"token": "Invalid token provided"},
                code=400
            )

        token_instance = Tokens.objects.get(token=token, is_valid=True)

        if not default_token_generator.check_token(token_instance.user, token):
            raise serializers.ValidationError(
                {"token": "Invalid token provided"},
                code=400
            )

        token_instance.user.is_active = True
        token_instance.is_valid = False
        token_instance.user.save()
        token_instance.save()

        return attrs


class OtpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = Otp
        fields = ['otp', 'email']

    def validate(self, attrs):
        email = attrs.get('email', None)
        otp = attrs.get('otp', None)

        if not email:
            """email not provided"""
            raise serializers.ValidationError(
                {"email": "Email needed"},
                code=400
            )

        if not otp:
            """otp not provided"""
            raise serializers.ValidationError(
                {"otp": "Otp needed"},
                code=400
            )

        if not get_user_model().objects.filter(email=email).exists():
            """user with this email does not exists"""
            raise serializers.ValidationError(
                {"email": "Invalid email provided"},
                code=400
            )

        user = get_user_model().objects.get(email=email)

        if not Otp.objects.filter(otp=otp, user=user).exists():
            """otp does not exists in database"""
            raise serializers.ValidationError(
                {"otp": "Invalid otp provided"},
                code=400
            )

        otp_instance = Otp.objects.get(otp=otp, user=user)

        if otp_instance.is_expired:
            """otp expired due to 5 min time line"""
            raise serializers.ValidationError(
                {"otp": "Otp expired"},
                code=400
            )

        if otp_instance.is_valid:
            """otp was verified before"""
            raise serializers.ValidationError(
                {"otp": "Otp expired"},
                code=400
            )

        otp_instance.is_valid = True
        otp_instance.save()

        return attrs


class OtpSerializerEmailOnly(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email', None)

        if not email:
            raise serializers.ValidationError(
                {"email": "No email provided"},
                code=400
            )

        if not get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Email is not registered"},
                code=400
            )

        otp = generate_secure_otp()
        user = get_user_model().objects.get(email=email)

        Otp.objects.create(otp=otp, user=user)

        return attrs


class OtpSerializerPassword(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = Otp
        fields = ['otp', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', None)
        otp = attrs.get('otp', None)
        password = attrs.get('password', None)

        if not email or not otp or not password:
            raise serializers.ValidationError(
                {"error": "Invalid data provided"},
                code=400
            )

        if not get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Email is not registered"},
                code=400
            )

        user = get_user_model().objects.get(email=email)

        if not Otp.objects.filter(otp=otp, user=user).exists():
            """otp does not exists in database"""
            raise serializers.ValidationError(
                {"otp": "Invalid otp provided"},
                code=400
            )

        otp_instance = Otp.objects.get(otp=otp, user=user)

        if not otp_instance.is_valid:
            """otp was not verified before"""
            raise serializers.ValidationError(
                {"otp": "Unverifed Otp provided"},
                code=400
            )

        user.set_password(password)
        user.save()

        return attrs


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if not email or not password:
            raise serializers.ValidationError(
                {"error": "Invalid input"},
                code=400
            )

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError(
                {"error": "Invalid email or password provided"},
                code=400
            )

        if not user.is_admin or not user.is_superuser:
            raise serializers.ValidationError(
                {"error": "You don't have permission to login"},
                code=400
            )

        return user
