from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from accounts.models import CustomUser


class FollowUser(models.Model):
    user_id = models.ForeignKey(CustomUser, related_name='follower', on_delete=models.CASCADE)

    following_user_id = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)

    class Meta:
        unique_together = [['user_id', 'following_user_id']]
