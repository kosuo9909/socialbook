import pyperclip
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView, DetailView, DeleteView

from core.forms import SignUpForm, SignInForm, PostForm, LikeForm, CommentForm
from core.models import Profile, PostMaker, LikePhoto, CommentPhoto, FollowUser

UserModel = get_user_model()


# Create your views here.
def index(request):
    all_photos = None
    liked_photos = None
    comment_form = CommentForm()
    all_users = UserModel.objects.all().order_by('-date_joined')
    all_profiles = Profile.objects.all()

    try:
        all_photos = PostMaker.objects.all()
        liked_photos = LikePhoto.objects.all()

    except:
        pass

    context = {
        'photos': all_photos,
        'likes': liked_photos,
        'comment_form': comment_form,
        'users': all_users[:5],
        'profiles': all_profiles,
    }
    return render(request, 'index.html', context=context)


class SignUp(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        login(self.request, self.object)
        return response


class SignIn(LoginView):
    template_name = 'signin.html'
    success_url = reverse_lazy('index')


class SignOut(LogoutView):
    next_page = reverse_lazy('index')


class DeleteProfile(DeleteView):
    model = UserModel
    context_object_name = 'delete_profile'
    success_url = reverse_lazy('index')


class SettingsProfile(UpdateView):
    template_name = 'setting.html'
    model = Profile

    fields = ('first_name', 'last_name', 'age', 'profileimg', 'timeline', 'location', 'bio')
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.object.pk == self.request.user.pk

        return context


class UpdateProfile(DetailView):
    template_name = 'profile.html'
    model = Profile

    fields = ('first_name', 'last_name', 'age', 'profileimg', 'location')
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.pk == self.request.user.pk
        context['object_user'] = self.object.user

        return context


class UploadPhoto(CreateView):
    template_name = 'upload.html'
    model = PostMaker
    fields = ['image', 'caption']

    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.pk
        form.instance.username = self.request.user.username
        return super().form_valid(form)


def delete_photo(request, pk):
    photo = PostMaker.objects.get(pk=pk)
    photo.delete()

    return redirect('index')


def like_photo(request, photo_id):
    try:
        LikePhoto.objects.create(
            user=request.user,
            photo=PostMaker.objects.get(pk=photo_id),
        )
    except IntegrityError:
        LikePhoto.objects.get(
            user=request.user,
            photo=PostMaker.objects.get(pk=photo_id),
        ).delete()

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')


@login_required
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

    return redirect('index')


def delete_comment(request, pk):
    comment = CommentPhoto.objects.get(pk=pk)
    comment.delete()

    return redirect('index')


def update_comment(request, pk):
    context = {}
    comment = get_object_or_404(CommentPhoto, pk=pk)

    form = CommentForm(request.POST or None, instance=comment)

    if form.is_valid():
        form.save()

    context['update_comment'] = form

    return render(request, 'index.html', context=context)


def follow_user(request, pk):
    try:
        new_follower = FollowUser.objects.create(
            user_id=UserModel.objects.get(pk=pk),
            following_user_id=UserModel.objects.get(pk=request.user.pk),

        )
    except IntegrityError:
        FollowUser.objects.get(user_id=UserModel.objects.get(pk=pk),
                               following_user_id=UserModel.objects.get(pk=request.user.pk)).delete()
    return redirect('update profile', pk=pk)


def copy_to_clipboard(request, photo_id):
    pyperclip.copy(f'{request.META["HTTP_REFERER"]}#{photo_id}')
    return redirect(f'{request.META["HTTP_REFERER"]}#{photo_id}')
