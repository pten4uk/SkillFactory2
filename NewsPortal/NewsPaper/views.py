from django.views.generic import ListView, DetailView

from .models import Post
from .filters import PostFilter


class NewsList(ListView):
    model = Post
    template_name = 'NewsPaper/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-datetime')
    paginate_by = 10

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'filter': self.get_filter()
        }


class NewsDetail(DetailView):
    model = Post
    template_name = 'NewsPaper/post.html'
    context_object_name = 'post'