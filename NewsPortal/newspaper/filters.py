import django_filters
from django import forms

from .models import Post


class PostFilter(django_filters.FilterSet):
    datetime = django_filters.DateTimeFilter(widget=(forms.TextInput(attrs={'type': 'date'})))

    class Meta:
        model = Post
        fields = {
            'datetime': ['exact'],
            'head': ['icontains'],
            'author': ['exact'],
        }