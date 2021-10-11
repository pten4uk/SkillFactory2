import pytz
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post, Author, Category
from .filters import PostFilter


class NewsList(ListView):
    model = Post
    template_name = 'newspaper/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-datetime')
    paginate_by = 10

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        context['filter'] = self.get_filter()
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('home')

# class NewsList(View):
#     def get(self, request, *args, **kwargs):



class NewsDetail(DetailView):
    model = Post
    template_name = 'newspaper/post.html'
    context_object_name = 'post'


class NewsCreate(LoginRequiredMixin, CreateView):
    template_name = 'newspaper/create.html'
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = Author.objects.get_or_create(user=self.request.user)[0]
        if not self.object.author.user.groups.filter(name='authors').exists():
            group, created = Group.objects.get_or_create(name='authors')
            group.user_set.add(self.request.user)
        self.object.save()

        cat = Category.objects.get(pk=self.request.POST['category'])
        self.object.category.add(cat)
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'newspaper/create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(LoginRequiredMixin, DeleteView):
    template_name = 'newspaper/delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


@login_required
def subscribe(r):
    categories = Category.objects.all()
    return render(r, 'newspaper/subscribe.html', {'categories': categories})


@login_required
def unsubscribe(r):
    r.user.subscribe_category = None
    r.user.save()
    return redirect('home')


@login_required
def choice_category_for_subscribe(r, pk):
    r.user.subscribe_category = Category.objects.get(pk=pk)
    r.user.save()
    return redirect('home')
