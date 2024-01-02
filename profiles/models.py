from accounts.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    profile_image = models.ImageField(blank=True, null=True, upload_to='profile_pics')
    header_image = models.ImageField(blank=True, null=True, upload_to='header_pics')
    username = models.CharField(max_length=50)
    display_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username.capitalize()}'s Profile"

    class Meta:
        ordering = ('-created_at',)