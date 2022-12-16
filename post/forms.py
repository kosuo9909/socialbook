from django import forms
from django.core.exceptions import ValidationError

from post.models import PostMaker, LikePhoto, CommentPhoto


class PostForm(forms.ModelForm):
    class Meta:
        model = PostMaker
        fields = ['image', 'caption']

    def clean_image(self):
        image = self.cleaned_data.get('image', None)

        if image:
            if image.size > 5*1024*1024:
                raise ValidationError('The image file is too large ( > 5 MB )')
            return image
        else:
            raise ValidationError('Could not read the uploaded image')


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