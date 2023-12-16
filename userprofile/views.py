from rest_framework.generics import RetrieveUpdateAPIView
from userprofile.serializer import UserProfilerSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["User Profile"])
class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfilerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """return authenticated user only"""
        return self.request.user
