from django.contrib.auth.decorators import login_required
from django.urls import path

from post.views import UploadPhoto, UpdatePost, delete_photo, like_photo, comment_photo, delete_comment

urlpatterns = (

    path('upload/', login_required(UploadPhoto.as_view()), name='upload photo'),
    path('edit/<int:pk>', login_required(UpdatePost.as_view()), name='update post'),
    path('delete/<int:pk>', login_required(delete_photo), name='delete photo'),
    path('like/<int:photo_id>', login_required(like_photo), name='like photo'),
    path('comment/<int:photo_id>', login_required(comment_photo), name='comment'),
    path('deletecomment/<int:pk>', login_required(delete_comment), name='delete comment'),
)
