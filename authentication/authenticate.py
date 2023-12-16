from rest_framework_simplejwt import authentication as jwt_authentication
from django.conf import settings


class CustomAuthentication(jwt_authentication.JWTAuthentication):
    def authenticate(self, request):
        raw_token = (
            request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        )

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
