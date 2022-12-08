import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.db.models.options import Options

# Create your models here.

User = get_user_model()


# class CustomUser(AbstractUser)


class Profile(models.Model):
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    age = models.IntegerField(
        validators=(
            validators.MinValueValidator(1, 'You are lying'),
        ),
        blank=True,
        null=True,
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, )
    # id_user = models.IntegerField()
    bio = models.TextField(blank=True,
                           null=False)
    profileimg = models.ImageField(upload_to='profile_images', default='profile_images/def2.png',
                                   verbose_name='Profile Picture',
                                   blank=True,
                                   null=True,
                                   )

    timeline = models.ImageField(upload_to='timeline_images', default='other/default_timeline.png',
                                   verbose_name='Timeline Picture',
                                   blank=True,
                                   null=True,
                                   )
    location = models.CharField(
        max_length=100,
        blank=True,
    )

    def __str__(self):
        return self.user.username


class PostMaker(models.Model):
    image = models.ImageField(
        upload_to='post_images',
        default='',
        verbose_name='Post Image',
        blank=False,
        null=False,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
    )

    username = models.CharField(
        max_length=50,
    )

    number_of_likes = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=datetime.datetime.now)

    caption = models.TextField(

    )


class LikePhoto(models.Model):
    photo = models.ForeignKey(PostMaker, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['photo', 'user']]


class CommentPhoto(models.Model):
    photo = models.ForeignKey(PostMaker, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.CharField(
        max_length=200,
        verbose_name='',
    )


class FollowUser(models.Model):
    user_id = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

    following_user_id = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)

    class Meta:
        unique_together = [['user_id', 'following_user_id']]
