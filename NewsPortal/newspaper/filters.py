import django_filters
from django import forms

from .models import Post


class PostFilter(django_filters.FilterSet):
    date = django_filters.DateTimeFilter(widget=(forms.TextInput(attrs={'type': 'date'})))

    class Meta:
        model = Post
        fields = {
            'date': ['exact'],
            'head': ['icontains'],
            'author': ['exact'],
        }
