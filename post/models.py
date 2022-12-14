from django.db import models
from django.db.models.functions import datetime

from accounts.models import CustomUser


class PostMaker(models.Model):
    class Meta:
        verbose_name_plural = 'Posts'

    image = models.ImageField(
        upload_to='post_images',
        default='',
        verbose_name='Post Image',
        blank=False,
        null=False,
    )

    user = models.ForeignKey(
        CustomUser,
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

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liker')

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owner')

    class Meta:
        unique_together = [['photo', 'user']]


class CommentPhoto(models.Model):
    photo = models.ForeignKey(PostMaker, on_delete=models.CASCADE)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    text = models.CharField(
        max_length=200,
        verbose_name='',
    )