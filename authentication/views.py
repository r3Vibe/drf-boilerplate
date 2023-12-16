from authentication.serializer import (
    UserModelSerializer,
    TokenSerializer,
    OtpSerializer,
    OtpSerializerEmailOnly,
    OtpSerializerPassword,
    AdminLoginSerializer,
)
from rest_framework.generics import CreateAPIView, GenericAPIView
from drf_spectacular.utils import extend_schema
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework.response import Response
from rest_framework import status
from authentication.helper import (
    get_user_tokens,
    refresh_token
)
from django.conf import settings
from authentication.authenticate import CustomAuthentication


@extend_schema(tags=["User Authentication"])
class LoginUserTokenView(TokenObtainPairView):
    """login user and send tokens"""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"


@extend_schema(tags=["User Authentication"])
class RefreshTokenPair(TokenRefreshView):
    """refresh the tokens"""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "refresh"


@extend_schema(tags=["User Authentication"])
class RegisterUser(CreateAPIView):
    """register new accounts"""

    serializer_class = UserModelSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "register"


@extend_schema(tags=["User Authentication"])
class VerifyAndActivateAccount(GenericAPIView):
    serializer_class = TokenSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "verify"

    def post(self, request):
        """verify the token and activate the account"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Account activated successfully"},
                status=status.HTTP_200_OK
            )


@extend_schema(tags=["Common Authentication"])
class ForgotPassword(GenericAPIView):
    """generate and verify otp then change the password of the user"""

    serializer_class = OtpSerializerEmailOnly
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "forgot"

    def post(self, request):
        """get the email of the user and generate otp"""
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Otp generated successfully"},
                status=status.HTTP_200_OK
            )


@extend_schema(tags=["Common Authentication"])
class ForgotPasswordVerifyOtp(GenericAPIView):
    """verify the otp"""

    serializer_class = OtpSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "forgot"

    def post(self, request):
        """verify the otp"""
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Otp verified successfully"},
                status=status.HTTP_200_OK
            )


@extend_schema(tags=["Common Authentication"])
class ForgotPasswordUpdate(GenericAPIView):
    """update the password"""

    serializer_class = OtpSerializerPassword
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "forgot"

    def patch(self, request):
        """update the password"""
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Password updated"},
                status=status.HTTP_200_OK
            )


@extend_schema(tags=["Admin Authentication"])
class LoginAdminUser(GenericAPIView):
    """admin auth will use cookies"""

    serializer_class = AdminLoginSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "adminlogin"

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            tokens = get_user_tokens(user)

            res = Response()

            res.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=tokens["access_token"],
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )

            res.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                value=tokens["refresh_token"],
                expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )

            return res


@extend_schema(tags=["Admin Authentication"])
class LogoutAdminUser(GenericAPIView):
    """logout the user"""

    serializer_class = AdminLoginSerializer
    authentication_classes = []
    permission_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "adminlogin"

    def post(self, request):
        """process the logout"""
        refreshToken = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            None
        )

        if refreshToken:
            token = refresh_token(refreshToken)
            token.blacklist()

        res = Response()
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])

        return res


@extend_schema(tags=["Admin Authentication"])
class RefreshAdminUser(GenericAPIView):
    """admin auth will use cookies"""

    serializer_class = AdminLoginSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "adminlogin"

    def post(self, request):
        refreshToken = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
        )
        token = refresh_token(refreshToken)
        token.blacklist()
        tokens = get_user_tokens(request.user)
        res = Response()
        res.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=tokens["access_token"],
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        res.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
            value=tokens["refresh_token"],
            expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        return res
