import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core import validators
from django.db import models
from django.utils import timezone

from core.managers import CustomUserManager
from core.validators import validate_letters


# Create your models here.

# User = get_user_model()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = 'Users'

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    username = models.CharField(
        unique=True,
        max_length=30,
        validators=(
            validators.MinLengthValidator(2),
            validate_letters,
        )
    )

    email = models.EmailField(
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()


def __str__(self):
    return self.email


class Profile(models.Model):
    class Meta:
        verbose_name_plural = 'Profiles'

    first_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        validators=(
            validators.MinLengthValidator(2),
            validate_letters,
        )
    )

    last_name = models.CharField(
        null=True,
        blank=True,
        max_length=30,
        validators=(
            validators.MinLengthValidator(2),
            validate_letters,
        )
    )

    age = models.IntegerField(
        validators=(
            validators.MinValueValidator(1, 'You are lying'),
        ),
        blank=True,
        null=True,
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, )
    # id_user = models.IntegerField()
    bio = models.TextField(blank=True,
                           null=False)
    profileimg = models.ImageField(upload_to='profile_images', default='defaults/def.png',
                                   verbose_name='Profile Picture',
                                   blank=True,
                                   null=True,
                                   )

    timeline = models.ImageField(upload_to='timeline_images', default='defaults/timeline1.png',
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


class FollowUser(models.Model):
    user_id = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)

    following_user_id = models.ForeignKey(CustomUser, related_name='follower', on_delete=models.CASCADE)

    class Meta:
        unique_together = [['user_id', 'following_user_id']]
