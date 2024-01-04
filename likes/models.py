from accounts.models import User
from comments.models import Comment
from django.db import models
from posts.models import Post


class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_liked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User - {self.user.username} - Liked - Post - {self.post.text}'

    class Meta():
        ordering = ('-time_liked',)


class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_liked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User - {self.user.username} - Liked - Comment - {self.comment.comment}'

    class Meta():
        ordering = ('-time_liked',)
