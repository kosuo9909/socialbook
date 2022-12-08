from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import Library

from core.models import LikePhoto

register = Library()


@register.simple_tag()
def get_obj(pk):
    obj = LikePhoto.objects.filter(photo_id=int(pk)).count()
    return obj


