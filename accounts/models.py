from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from accounts.managers import CustomUserManager
from core.validators import validate_letters


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
    bio = models.TextField(blank=True,
                           null=False)
    profileimg = models.ImageField(upload_to='profile_images', default='defaults/def.png',
                                   verbose_name='Profile Picture',
                                   blank=True,
                                   null=True,
                                   )

    timeline = models.ImageField(upload_to='timeline_images', default='defaults/pythonweb-timeline.png',
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


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
