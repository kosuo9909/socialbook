from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import Profile

UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'username')

    # def save(self, commit=True):
    #     user = super().save(commit=commit)
    #     profile = Profile(
    #         user=user,
    #     )
    #     if commit:
    #         profile.save()
    #     return user


class SignInForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username','email')


class CustomUserEditForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ('username','email')

