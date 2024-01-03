from .models import Comment
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'comment', 'image', 'user', 'date_commented', 'time_commented']

    def get_user(self, obj):
        return obj.user.username if obj.user else None

    def get_post(self, obj):
        return obj.post.text if obj.post else None