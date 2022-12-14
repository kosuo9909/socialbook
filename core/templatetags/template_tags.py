
from django.template import Library

from post.models import LikePhoto

register = Library()


@register.simple_tag()
def get_obj(pk):
    obj = LikePhoto.objects.filter(photo_id=int(pk)).count()
    return obj


