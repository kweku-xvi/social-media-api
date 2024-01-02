from .models import Profile
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['profile_image', 'header_image', 'username', 'display_name', 'bio', 'location', 'website', 'user']

        read_only_fields = ['username', 'user']

    def get_user(self, obj):
        return obj.user.username if obj.user else None