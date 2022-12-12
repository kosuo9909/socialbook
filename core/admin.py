from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import SignUpForm, CustomUserEditForm
from .models import Profile, PostMaker, CustomUser

# Register your models here.
# UserModel = get_user_model()

admin.site.register(Profile)
admin.site.register(PostMaker)


class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = CustomUserEditForm
    model = CustomUser

    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('username', 'email', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
