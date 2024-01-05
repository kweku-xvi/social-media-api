from accounts.models import User
from django.db import models

class FollowUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    time_followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} follows {self.user.username}'

    class Meta:
        ordering = ('-time_followed',)
