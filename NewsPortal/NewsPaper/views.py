from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post, Author
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
            'filter': self.get_filter(),
            'is_not_author': not self.request.user.groups.filter(name='authors').exists()
        }


class NewsDetail(DetailView):
    model = Post
    template_name = 'NewsPaper/post.html'
    context_object_name = 'post'


class NewsCreate(LoginRequiredMixin, CreateView):
    template_name = 'NewsPaper/create.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='authors').exists():
            group = Group.objects.get(name='authors')
            group.user_set.add(self.request.user)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.author = Author.objects.get_or_create(polzovatel=self.request.user)[0]
        if not self.object.author.polzovatel.groups.filter(name='authors').exists():
            group = Group.objects.get(name='authors')
            group.user_set.add(self.request.user)
        self.object.save()
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'NewsPaper/create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(LoginRequiredMixin, DeleteView):
    template_name = 'NewsPaper/delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'