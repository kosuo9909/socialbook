from django.contrib.auth.decorators import login_required
from django.urls import path

from core.views import index, SignUp, SignIn, SignOut, UpdateProfile, UploadPhoto, delete_photo, like_photo, \
    comment_photo, delete_comment, update_comment, SettingsProfile, follow_user, copy_to_clipboard, DeleteProfile, \
    UpdatePost

urlpatterns = (

    path('', index, name='index'),
    path('register/', SignUp.as_view(), name='register'),
    path('login/', SignIn.as_view(), name='login'),
    path('logout/', login_required(SignOut.as_view()), name='logout'),
    path('profile/<int:pk>', UpdateProfile.as_view(), name='update profile'),
    path('settings/<int:pk>', login_required(SettingsProfile.as_view()), name='settings profile'),
    path('upload/', login_required(UploadPhoto.as_view()), name='upload photo'),
    path('edit/<int:pk>', login_required(UpdatePost.as_view()), name='update post'),
    path('delete/<int:pk>', login_required(delete_photo), name='delete photo'),
    path('like/<int:photo_id>', login_required(like_photo), name='like photo'),
    path('comment/<int:photo_id>', login_required(comment_photo), name='comment'),
    path('deletecomment/<int:pk>', login_required(delete_comment), name='delete comment'),
    path('updatecomment/<int:pk>', login_required(update_comment), name='update comment'),
    path('follow/<int:pk>', login_required(follow_user), name='follow user'),
    path('copy/<int:photo_id>', copy_to_clipboard, name='copy'),
    path('delete_profile/<int:pk>', login_required(DeleteProfile.as_view()),name='delete profile' ),

)

