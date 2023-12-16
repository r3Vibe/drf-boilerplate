from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserProfilerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"
        extra_kwargs = {'password': {"write_only": True}}

    def update(self, instance, validated_data):
        """update the user model"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
