from django.urls import path
from authentication.views import (
    LoginUserTokenView,
    RefreshTokenPair,
    RegisterUser,
    VerifyAndActivateAccount,
)


app_name = "authentication_user"


urlpatterns = [
    path('login/', LoginUserTokenView.as_view(), name='login'),
    path('refresh/', RefreshTokenPair.as_view(), name='refresh'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('verify/', VerifyAndActivateAccount.as_view(), name='verify'),
]
