import uuid
from accounts.models import User
from django.db import models

class Post(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    text = models.CharField(max_length=1500)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    date_posted = models.DateField(auto_now_add=True)
    time_posted = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text}"

    class Meta:
        ordering = ('-created_at',)
