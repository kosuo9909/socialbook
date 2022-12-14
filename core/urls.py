from django.contrib.auth.decorators import login_required
from django.urls import path

from core.views import index, UpdateProfile, \
    SettingsProfile, follow_user, copy_to_clipboard, DeleteProfile

urlpatterns = (

    path('', index, name='index'),
    path('profile/<int:pk>', UpdateProfile.as_view(), name='update profile'),
    path('settings/<int:pk>', login_required(SettingsProfile.as_view()), name='settings profile'),
    path('follow/<int:pk>', login_required(follow_user), name='follow user'),
    path('copy/<int:photo_id>', copy_to_clipboard, name='copy'),
    path('delete_profile/<int:pk>', login_required(DeleteProfile.as_view()),name='delete profile' ),

)

