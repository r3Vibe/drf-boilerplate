from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.views import root

urlpatterns = [
    path("", root, name="home"),
    path("api/docs/", SpectacularSwaggerView.as_view(), name="swagger"),
    path("api/docs/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/auth/", include("authentication.urls")),
    path("api/profile/", include("userprofile.urls")),
]
