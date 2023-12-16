from django.urls import path, include

urlpatterns = [
    path('users/', include('authentication.user_urls')),
    path('admin/', include('authentication.admin_urls')),
    path('common/', include('authentication.common_urls')),
]
