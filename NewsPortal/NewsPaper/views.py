from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    template_name = 'NewsPaper/news.html'
    context_object_name = 'news'


class NewsDetail(DetailView):
    model = Post
    template_name = 'NewsPaper/post.html'
    context_object_name = 'post'