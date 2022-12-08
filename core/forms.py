from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from core.models import Profile, PostMaker, LikePhoto, CommentPhoto

UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username',)

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            user=user,
        )
        if commit:
            profile.save()
        return user


class SignInForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username',)


class PostForm(forms.ModelForm):
    class Meta:
        model = PostMaker
        fields = ['image', 'caption']


class LikeForm(forms.ModelForm):
    class Meta:
        model = LikePhoto
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentPhoto
        fields = ['text']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for key, field in self.fields.items():
                field.label = ""