from django.urls import path
from authentication.views import (
    LoginAdminUser,
    RefreshAdminUser,
    LogoutAdminUser
)


app_name = "authentication_admin"


urlpatterns = [
    path('login/', LoginAdminUser.as_view(), name='login'),
    path('logout/', LogoutAdminUser.as_view(), name='logout'),
    path('refresh/', RefreshAdminUser.as_view(), name='refresh'),
]
