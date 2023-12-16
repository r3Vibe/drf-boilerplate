from django.urls import path
from authentication.views import (
    ForgotPassword,
    ForgotPasswordVerifyOtp,
    ForgotPasswordUpdate
)


app_name = "authentication_common"


urlpatterns = [
    path('forgot-password/', ForgotPassword.as_view(), name='forgot-password'),
    path('verify-otp/', ForgotPasswordVerifyOtp.as_view(), name='verify-otp'),
    path(
        'reset-password/',
        ForgotPasswordUpdate.as_view(),
        name='reset-password'
    ),
]
