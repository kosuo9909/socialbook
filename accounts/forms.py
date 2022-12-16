from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'username')


class SignInForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email')


class CustomUserEditForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email')
