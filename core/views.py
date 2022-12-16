import pyperclip
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, DeleteView

import core.models
from accounts.models import Profile
from core.models import FollowUser
from post.forms import CommentForm
from post.models import PostMaker, LikePhoto

UserModel = get_user_model()


def index(request):
    found_users = None
    given_query = None
    comment_form = CommentForm()
    all_users = UserModel.objects.all().order_by('-date_joined')
    all_profiles = Profile.objects.all()
    liked_photos = LikePhoto.objects.all()
    all_photos = PostMaker.objects.all()
    p = Paginator(all_photos.reverse(), 10)

    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    try:

        found_users = UserModel.objects.filter(username__icontains=request.GET.get('find_user'))
        given_query = request.GET.get('find_user')

    except:
        pass

    context = {
        'photos': all_photos,
        'likes': liked_photos,
        'comment_form': comment_form,
        'users': all_users[:5],
        'profiles': all_profiles,
        'found_users': found_users,
        'user_find_query': given_query,
        'page_obj': page_obj,
    }
    return render(request, 'index.html', context=context)


class DeleteProfile(UserPassesTestMixin, DeleteView):
    model = UserModel
    context_object_name = 'delete_profile'
    success_url = reverse_lazy('index')

    def test_func(self):
        my_object = self.get_object()
        return my_object == self.request.user


class SettingsProfile(UpdateView):
    template_name = 'setting.html'
    model = Profile

    fields = ('first_name', 'last_name', 'age', 'profileimg', 'timeline', 'location', 'bio')

    def get_success_url(self):
        return reverse_lazy('update profile', kwargs={'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.object.pk == self.request.user.pk

        return context

    def form_valid(self, form):
        return super(SettingsProfile, self).form_valid(form)


class UpdateProfile(DetailView):
    template_name = 'profile.html'
    model = Profile

    fields = ('first_name', 'last_name', 'age', 'profileimg', 'location')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.pk == self.request.user.pk
        context['object_user'] = self.object.user
        try:
            context['already_following'] = True if self.request.user.following.get(
                user_id_id=self.object.user.pk) else False
        except core.models.FollowUser.DoesNotExist:
            pass
        # print(self.object.user.follower.get(user_id_id=self.request.user.pk))
        # test = self.request.user.follower.get(user_id_id=1)
        # print(test)

        return context


def follow_user(request, pk):
    try:
        FollowUser.objects.create(
            user_id=UserModel.objects.get(pk=pk),
            following_user_id=UserModel.objects.get(pk=request.user.pk),

        )
    except IntegrityError:
        FollowUser.objects.get(user_id=UserModel.objects.get(pk=pk),
                               following_user_id=UserModel.objects.get(pk=request.user.pk)).delete()
    return redirect('update profile', pk=pk)


def copy_to_clipboard(request, photo_id):
    pyperclip.copy(f'{request.META["HTTP_REFERER"]}#photo-{photo_id}')
    return redirect(f'{request.META["HTTP_REFERER"]}#photo-{photo_id}')
