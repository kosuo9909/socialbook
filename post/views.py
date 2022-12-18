from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from post.forms import CommentForm
from post.models import PostMaker, LikePhoto, CommentPhoto


class UploadPhoto(CreateView):
    template_name = 'upload.html'
    model = PostMaker
    fields = ['image', 'caption']

    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.pk
        form.instance.username = self.request.user.username
        return super().form_valid(form)


class UpdatePost(UserPassesTestMixin,UpdateView):

    template_name = 'update-post.html'
    model = PostMaker
    fields = ['image', 'caption']

    success_url = reverse_lazy('index')

    def test_func(self):
        my_object = self.get_object()
        return my_object.user == self.request.user or self.request.user.is_superuser


def delete_photo(request, pk):
    photo = PostMaker.objects.get(pk=pk)
    if photo.user.pk == request.user.pk or request.user.is_superuser:
        photo.delete()
    else:
        raise PermissionDenied()

    return redirect('index')


def like_photo(request, photo_id):
    try:
        photo = PostMaker.objects.get(pk=photo_id)
        photo_owner = photo.user
        LikePhoto.objects.create(
            user=request.user,
            photo=PostMaker.objects.get(pk=photo_id),
            owner=photo_owner,
        )
    except IntegrityError:
        LikePhoto.objects.get(
            user=request.user,
            photo=PostMaker.objects.get(pk=photo_id),
            owner=photo_owner,
        ).delete()

    return redirect(f'{request.META["HTTP_REFERER"]}#photo-{photo_id}')



def comment_photo(request, photo_id):
    photo = PostMaker.objects.get(pk=photo_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)  # Does not persist to DB
        comment.photo = photo
        comment.user = request.user
        comment.save()
    else:
        print('INVALID')

    return redirect(f'{request.META["HTTP_REFERER"]}#photo-{photo_id}')


def delete_comment(request, pk):
    comment = CommentPhoto.objects.get(pk=pk)

    if comment.user.pk == request.user.pk or request.user.is_superuser:
        comment.delete()
    else:
        raise PermissionDenied()

    return redirect(f'{request.META["HTTP_REFERER"]}#photo-{pk}')
