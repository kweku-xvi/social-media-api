import uuid
from accounts.models import User
from posts.models import Post
from django.db import models


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    comment = models.CharField(max_length=1500)
    image = models.ImageField(upload_to='comments', blank=True, null=True)
    date_commented = models.DateField(auto_now_add=True)
    time_commented = models.TimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - Comment: "{self.comment}" On Post: "{self.post.text}"'

    class Meta:
        ordering = ('-created_at',)