from rest_framework_simplejwt import tokens


def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }


def refresh_token(token):
    return tokens.RefreshToken(token)
