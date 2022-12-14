from django import forms

from post.models import PostMaker, LikePhoto, CommentPhoto


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