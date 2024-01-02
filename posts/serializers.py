from .models import Post
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'text', 'image', 'date_posted', 'time_posted', 'user']

    def get_user(self, obj):
        return obj.user.username if obj.user else None