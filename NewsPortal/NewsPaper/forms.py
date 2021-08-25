from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['type', 'head', 'text']


class UserSignupForm(SignupForm):

    def save(self, request):
        user = super().save(request)
        group = Group.objects.get(name='common')
        group.user_set.add(user)
        return user